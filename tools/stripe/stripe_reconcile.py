#!/usr/bin/env python3
"""Audit or reconcile Stripe against tools/stripe/manifest.json (non-live environments only).

    python3 tools/stripe/stripe_reconcile.py audit [--env dev|staging] [--product NAME]
    python3 tools/stripe/stripe_reconcile.py apply [--env ...] [--product ...] [--create-webhooks]

`audit` is read-only and exits 1 when anything has drifted. `apply` fixes what Stripe lets us
fix in place (products, prices, webhook events, portal features). A webhook endpoint's
api_version cannot be changed, so a mismatched or missing endpoint is created only with
--create-webhooks, and its signing secret is written to functions/.secret.local
(<ENV>_<PRODUCT>_WEBHOOK_SECRET), never printed.

Keys are read from functions/.secret.local (gitignored). Live mode is out of scope by design:
the script refuses any key that is not sk_test_/rk_test_.
"""
import argparse, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SECRETS = ROOT / "functions" / ".secret.local"
MANIFEST = json.loads((pathlib.Path(__file__).parent / "manifest.json").read_text())


def load_env():
    env = {}
    for line in SECRETS.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "/")) and "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    return env


def api(key, method, path, data=()):
    # System curl, not urllib: the framework Python on macOS lacks CA certificates.
    cmd = ["curl", "-s", "-u", key + ":", "-X", method, "https://api.stripe.com/v1/" + path]
    for k, v in data:
        cmd += ["-d", f"{k}={v}"]
    out = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout or "{}")
    if "error" in out:
        raise SystemExit(f"Stripe error on {method} {path}: {out['error'].get('message')}")
    return out


def listing(key, path):
    return api(key, "GET", path + ("&" if "?" in path else "?") + "limit=100").get("data", [])


class Run:
    def __init__(self, apply, create_webhooks):
        self.apply, self.create_webhooks, self.drift = apply, create_webhooks, 0

    def report(self, ok, msg, fixed=False):
        if ok:
            print(f"   ok      {msg}")
        else:
            self.drift += 0 if fixed else 1
            print(f"   {'fixed ' if fixed else 'DRIFT '}  {msg}")


def check_product(run, key, name, spec):
    if not spec.get("name"):
        return
    products = [p for p in listing(key, "products?active=true") if p["name"] == spec["name"]]
    product = products[0] if products else None
    if not product and run.apply:
        product = api(key, "POST", "products", [("name", spec["name"]), ("metadata[app]", name)])
    run.report(bool(products), f"product '{spec['name']}'", fixed=bool(product) and not products)
    if not product:
        return
    prices = {p["lookup_key"]: p for p in listing(key, f"prices?product={product['id']}&active=true") if p.get("lookup_key")}
    for want in spec["prices"]:
        have = prices.get(want["lookupKey"])
        good = bool(have) and have["unit_amount"] == want["amount"] and have["recurring"]["interval"] == want["interval"] and have["currency"] == "usd"
        if not good and run.apply and not have:
            api(key, "POST", "prices", [("product", product["id"]), ("currency", "usd"), ("unit_amount", want["amount"]),
                                         ("recurring[interval]", want["interval"]), ("lookup_key", want["lookupKey"]),
                                         ("metadata[app]", name)])
            run.report(False, f"price {want['lookupKey']} created", fixed=True)
        else:
            run.report(good, f"price {want['lookupKey']} ${want['amount'] / 100:g}/{want['interval']}" + ("" if good else " (wrong or missing; prices are immutable, create a new one and move the lookup key)"))


def check_webhook(run, key, env_name, name, spec, env):
    wh = spec["webhook"]
    host = wh["hosts"].get(env_name)
    if not host:
        return
    url = f"https://{host}{wh['path']}"
    endpoints = {w["url"]: w for w in listing(key, "webhook_endpoints")}
    ep = endpoints.get(url)
    if not ep:
        run.report(False, f"webhook endpoint {url} missing")
        if run.apply and run.create_webhooks:
            created = api(key, "POST", "webhook_endpoints", [("url", url), ("api_version", MANIFEST["apiVersion"]),
                                                             *[("enabled_events[]", e) for e in wh["events"]],
                                                             ("metadata[app]", name)])
            with SECRETS.open("a") as f:
                f.write(f"\n{env['keyPrefix']}_{name.upper().replace('-', '_')}_WEBHOOK_SECRET={created['secret']}\n")
            print(f"   fixed   webhook endpoint created; signing secret saved to functions/.secret.local")
            run.drift -= 1
        return
    if ep["api_version"] != MANIFEST["apiVersion"]:
        run.report(False, f"webhook {url} api_version {ep['api_version']} != {MANIFEST['apiVersion']} (cannot be changed in place: recreate the endpoint)")
    else:
        run.report(True, f"webhook {url} api_version {ep['api_version']}")
    if ep["status"] != "enabled":
        run.report(False, f"webhook {url} status {ep['status']}")
    want, have = set(wh["events"]), set(ep["enabled_events"])
    if want == have:
        run.report(True, f"webhook events ({len(want)})")
    elif run.apply:
        api(key, "POST", f"webhook_endpoints/{ep['id']}", [("enabled_events[]", e) for e in sorted(want)])
        run.report(False, f"webhook events updated (+{sorted(want - have)} -{sorted(have - want)})", fixed=True)
    else:
        run.report(False, f"webhook events differ (missing {sorted(want - have)}, extra {sorted(have - want)})")


def check_portal(run, key, name, spec):
    portal = spec.get("portal")
    if not portal:
        return
    configs = [c for c in listing(key, "billing_portal/configurations?active=true") if c.get("name") == portal["name"]]
    feats = [("features[payment_method_update][enabled]", "true"), ("features[invoice_history][enabled]", "true"),
             ("features[subscription_cancel][enabled]", "true"), ("features[subscription_cancel][mode]", portal["cancelMode"])]
    if not configs:
        if run.apply:
            api(key, "POST", "billing_portal/configurations", [("name", portal["name"]), *feats,
                                                                ("business_profile[headline]", portal["name"].title())])
        run.report(False, f"portal configuration '{portal['name']}' " + ("created" if run.apply else "missing"), fixed=run.apply)
        return
    f = configs[0]["features"]
    good = (f["payment_method_update"]["enabled"] and f["invoice_history"]["enabled"] and f["subscription_cancel"]["enabled"]
            and f["subscription_cancel"].get("mode") == portal["cancelMode"])
    if not good and run.apply:
        api(key, "POST", f"billing_portal/configurations/{configs[0]['id']}", feats)
    run.report(good, f"portal '{portal['name']}' (cancel {portal['cancelMode']})", fixed=(not good) and run.apply)


def check_account(run, key):
    acct = api(key, "GET", "account")
    bp = acct.get("business_profile") or {}
    want = MANIFEST["account"]
    run.report(bp.get("support_email") == want["supportEmail"], f"support email {bp.get('support_email')!r} (want {want['supportEmail']!r}; Dashboard only)")
    run.report(bp.get("support_url") == want["supportUrl"], f"support url {bp.get('support_url')!r} (want {want['supportUrl']!r}; Dashboard only)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["audit", "apply"])
    ap.add_argument("--env", choices=list(MANIFEST["environments"]))
    ap.add_argument("--product", choices=list(MANIFEST["products"]))
    ap.add_argument("--create-webhooks", action="store_true")
    args = ap.parse_args()
    env = load_env()
    run = Run(args.command == "apply", args.create_webhooks)
    for env_name, cfg in MANIFEST["environments"].items():
        if args.env and args.env != env_name:
            continue
        key = env.get(cfg["keyPrefix"] + "_SECRET_KEY", "")
        if not key.startswith(("sk_test_", "rk_test_")):
            raise SystemExit(f"{env_name}: {cfg['keyPrefix']}_SECRET_KEY missing or not a test key; refusing to run")
        print(f"== {env_name}")
        check_account(run, key)
        for name, spec in MANIFEST["products"].items():
            if args.product and args.product != name:
                continue
            print(f" -- {name}")
            check_product(run, key, name, spec)
            check_webhook(run, key, env_name, name, spec, cfg)
            check_portal(run, key, name, spec)
    print(f"\n{run.drift} item(s) still drifted")
    sys.exit(1 if run.drift else 0)


if __name__ == "__main__":
    main()
