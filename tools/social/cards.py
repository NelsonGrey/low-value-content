"""HTML templates for the social cards. Pure functions: data in, HTML string out.

Every card is a fixed-size HTML page rendered to an image by build_social.py. Colours and the
double-rule frame follow the website and docs/brand/LOW_VALUE_CONTENT_GUIDE.md (the shared House frame).
"""
from html import escape as e

ASSETS = "website/public/assets"

CSS = """
:root{--navy:#0d1c2b;--navy2:#142b40;--gold:#ba8d3a;--gold-l:#dabf83;--gold-t:#8a6417;--ivory:#f4eedf;--paper:#fbf7ed;--crimson:#852e34;--ink:#17202a;
--serif:Georgia,'Times New Roman',serif;--sans:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;--script:'Snell Roundhand','Apple Chancery',cursive}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:var(--bg)}
body{font-family:var(--serif);color:var(--fg);position:relative;-webkit-font-smoothing:antialiased}
.frame{position:absolute;inset:36px;border:4px double var(--gold)}
.dia{position:absolute;width:20px;height:20px;background:var(--gold);transform:rotate(45deg)}
.dia.tl{left:26px;top:26px}.dia.tr{right:26px;top:26px}.dia.bl{left:26px;bottom:26px}.dia.br{right:26px;bottom:26px}
.top{position:absolute;left:0;right:0;top:78px;display:flex;align-items:center;justify-content:center;gap:16px;font:700 21px/1 var(--sans);letter-spacing:.24em;text-transform:uppercase;color:var(--lab)}
.top img{width:46px;height:46px}
.bottom{position:absolute;left:0;right:0;bottom:76px;text-align:center}
.bottom .by{font:34px/1 var(--script);color:var(--byc)}
.bottom .st{margin-top:14px;font:700 18px/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--stc)}
.eyebrow{font:700 24px/1.3 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:var(--eb)}
.script{font-family:var(--script);font-weight:400}
.latin{font:700 24px/1.4 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--lat)}
.disc{border-radius:50%%;background:var(--ivory);border:6px solid var(--gold);display:grid;place-items:center}
.ivory{--bg:var(--ivory);--fg:var(--ink);--lab:var(--navy);--byc:var(--crimson);--stc:#4f5963;--eb:var(--crimson);--lat:var(--gold-t)}
.paper{--bg:var(--paper);--fg:var(--ink);--lab:var(--navy);--byc:var(--crimson);--stc:#4f5963;--eb:var(--crimson);--lat:var(--gold-t)}
.navy{--bg:var(--navy);--fg:var(--ivory);--lab:var(--gold-l);--byc:var(--gold-l);--stc:rgba(244,238,223,.75);--eb:var(--gold-l);--lat:var(--gold-l)}
.crimson{--bg:var(--crimson);--fg:#fff;--lab:var(--gold-l);--byc:var(--gold-l);--stc:rgba(255,255,255,.8);--eb:var(--gold-l);--lat:var(--gold-l)}
"""

def page(w, h, theme, body, extra_css=""):
    css = CSS % {"w": w, "h": h}
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}{extra_css}</style></head>"
            f"<body class='{theme}'>{body}</body></html>")

def chrome(status=None, theme_mark="royal-mark.svg"):
    """Frame, corner diamonds, House lockup at top, maker line at bottom."""
    st = f"<div class='st'>{e(status)}</div>" if status else ""
    return (f"<div class='frame'></div><i class='dia tl'></i><i class='dia tr'></i><i class='dia bl'></i><i class='dia br'></i>"
            f"<div class='top'><img src='{ASSETS}/{theme_mark}' alt=''><span>The Royal House of Engagement</span></div>"
            f"<div class='bottom'><div class='by'>Purveyed by Low Value Content</div>{st}</div>")

# ---------------------------------------------------------------- feed cards (1080 x 1350)
W, H = 1080, 1350

def calendar_card(day, month, name, year, line, latin, device, dark=False):
    css = """
.cal-eb{position:absolute;left:110px;top:200px}
.cal-date{position:absolute;left:104px;top:250px;display:flex;align-items:flex-end;gap:22px}
.cal-date .d{font-size:300px;line-height:.78;color:var(--crimson);letter-spacing:-.04em}
.cal-date .m{font:700 34px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;padding-bottom:14px;color:var(--fg)}
.cal-dev{position:absolute;right:110px;top:236px;width:250px;height:250px}
.cal-dev img{width:150px}
.cal-body{position:absolute;left:110px;right:110px;top:580px}
.cal-body h1{font-weight:400;font-size:96px;line-height:1.02;letter-spacing:-.02em;text-wrap:balance}
.cal-body .latin{margin-top:26px}
.cal-body p.l{margin-top:38px;font-size:46px;line-height:1.36;max-width:860px;opacity:.92}
.cal-est{position:absolute;left:110px;bottom:200px;font:700 22px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--eb)}
.navy .cal-date .d{color:var(--gold-l)}
"""
    lat = f"<p class='latin'>{e(latin)}</p>" if latin else ""
    body = (chrome() +
        "<p class='eyebrow cal-eb'>From the Royal Calendar</p>"
        f"<div class='cal-date'><span class='d'>{day:02d}</span><span class='m'>{e(month)}</span></div>"
        f"<div class='cal-dev disc'><img src='{ASSETS}/{device}' alt=''></div>"
        f"<div class='cal-body'><h1>{e(name)}</h1>{lat}<p class='l'>{e(line)}</p></div>"
        f"<p class='cal-est'>Established {e(year)}</p>")
    return page(W, H, "navy" if dark else "ivory", body, css)

def house_card(num, name, standing, contradiction, institution, latin, motto, badge):
    css = """
.h-badge{position:absolute;left:50%;top:150px;transform:translateX(-50%);width:430px;height:430px;display:grid;place-items:center}
.h-badge img{width:380px}
.stack{position:absolute;left:90px;right:90px;top:610px;bottom:190px;display:flex;flex-direction:column;align-items:center;text-align:center}
.h-name{margin-top:18px;font-weight:400;font-size:98px;line-height:1;letter-spacing:-.02em;text-wrap:balance}
.h-stand{margin-top:16px;font:62px/1.1 var(--script);color:var(--gold-l)}
.h-quote{margin-top:44px;max-width:840px;font-style:italic;font-size:42px;line-height:1.3;text-wrap:balance}
.h-inst{position:absolute;left:0;right:0;bottom:0}
.h-inst .latin{display:block;margin-top:14px}
"""
    body = (chrome() +
        f"<div class='h-badge'><img src='{ASSETS}/{badge}' alt=''></div>"
        f"<div class='stack'><p class='eyebrow'>The Six Great Houses · No. {num:02d}</p>"
        f"<h1 class='h-name'>{e(name)}</h1><p class='h-stand'>{e(standing)}</p>"
        f"<p class='h-quote'>\u201c{e(contradiction)}\u201d</p>"
        f"<div class='h-inst'><span class='eyebrow' style='font-size:20px'>{e(institution)}</span><span class='latin' style='font-size:21px'>{e(latin)} \u00b7 {e(motto)}</span></div></div>")
    return page(W, H, "navy", body, css)

def lineage_card(numeral, name, period, motto, account, device, disputed=False, present=False):
    tag = ""
    if disputed: tag = "Disputed succession"
    if present: tag = "The present reign"
    tagh = f"<div class='tag'>{e(tag)}</div>" if tag else ""
    css = """
.l-dev{position:absolute;left:50%;top:190px;transform:translateX(-50%);width:390px;height:390px}
.l-dev img{width:280px}
.stack{position:absolute;left:90px;right:90px;top:620px;bottom:190px;display:flex;flex-direction:column;align-items:center;text-align:center}
.l-name{margin-top:18px;font-weight:400;font-size:92px;line-height:1.02;letter-spacing:-.02em;text-wrap:balance}
.l-per{margin-top:14px;font:50px/1 var(--script);color:var(--gold-l)}
.l-acc{margin-top:34px;max-width:840px;font-size:37px;line-height:1.38;opacity:.95;text-wrap:balance}
.l-lat{position:absolute;left:0;right:0;bottom:0}
.tag{position:absolute;left:50%;top:146px;transform:translateX(-50%);padding:10px 18px;border:2px solid var(--gold-l);color:var(--gold-l);font:700 18px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;background:var(--crimson);z-index:3;white-space:nowrap}
"""
    body = (chrome() + tagh +
        f"<div class='l-dev disc'><img src='{ASSETS}/{device}' alt=''></div>"
        f"<div class='stack'><p class='eyebrow'>The Lineage of Engagement \u00b7 Reign {e(numeral)}</p>"
        f"<h1 class='l-name'>{e(name)}</h1><p class='l-per'>{e(period)}</p>"
        f"<p class='l-acc'>{e(account)}</p><p class='latin l-lat'>{e(motto)}</p></div>")
    return page(W, H, "crimson", body, css)

def principle_card(num, text, dark=False):
    css = """
.p-n{position:absolute;left:0;right:0;top:230px;text-align:center}
.p-orn{position:absolute;left:50%;top:300px;transform:translateX(-50%);width:110px;height:110px}
.p-orn img{width:100%}
.p-mid{position:absolute;left:110px;right:110px;top:440px;bottom:330px;display:flex;align-items:center;justify-content:center}
.p-t{text-align:center;font-weight:400;font-size:104px;line-height:1.08;letter-spacing:-.02em;text-wrap:balance}
.p-rule{position:absolute;left:50%;top:1110px;width:200px;height:2px;background:var(--gold);transform:translateX(-50%)}
.p-sig{position:absolute;left:0;right:0;top:1140px;text-align:center}
"""
    body = (chrome() +
        f"<p class='eyebrow p-n'>Constitutional principle No. {num:02d}</p>"
        f"<div class='p-orn'><img src='{ASSETS}/royal-mark.svg' alt=''></div>"
        f"<div class='p-mid'><h1 class='p-t'>{e(text)}</h1></div><div class='p-rule'></div>"
        "<p class='script p-sig' style='font-size:40px;color:var(--byc)'>By Sovereign Instrument</p>")
    return page(W, H, "navy" if dark else "ivory", body, css)

def product_card(num, title, subtitle, art, garment, status="In development · not yet for sale"):
    css = f"""
.pr-eb{{position:absolute;left:0;right:0;top:158px;text-align:center}}
.pr-panel{{position:absolute;left:50%;top:205px;transform:translateX(-50%);width:640px;height:780px;background:{garment};border:2px solid var(--gold);box-shadow:0 20px 50px rgba(13,28,43,.25);display:grid;place-items:center}}
.pr-panel img{{width:600px;height:730px;object-fit:contain}}
.pr-text{{position:absolute;left:100px;right:100px;top:1006px;bottom:190px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.pr-t{{font-weight:400;font-size:52px;line-height:1.1;text-wrap:balance}}
.pr-sub{{margin-top:14px;font:italic 30px/1.2 var(--serif);color:var(--crimson)}}
"""
    body = (chrome(status=status) +
        f"<p class='eyebrow pr-eb'>The founding collection · No. {num:02d}</p>"
        f"<div class='pr-panel'><img src='{ASSETS}/{art}' alt=''></div>"
        f"<div class='pr-text'><h1 class='pr-t'>{e(title)}</h1><p class='pr-sub'>{e(subtitle)}</p></div>")
    return page(W, H, "ivory", body, css)

def photo_card(src, ribbon="Concept mockup · in development"):
    css = f"""
html,body{{background:#000}}
.ph{{position:absolute;inset:0;background:url('{src}') center/cover no-repeat}}
.ph::after{{content:'';position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(transparent,rgba(13,28,43,.88))}}
.rb{{position:absolute;left:0;right:0;bottom:44px;text-align:center;z-index:2;color:#f4eedf;font:700 20px/1 var(--sans);letter-spacing:.22em;text-transform:uppercase}}
"""
    body = f"<div class='ph'></div><div class='rb'>{e(ribbon)}</div>"
    return page(W, H, "navy", body, css)

def plate_card(src, plate, title, caption):
    css = f"""
.pl-eb{{position:absolute;left:0;right:0;top:160px;text-align:center}}
.pl-img{{position:absolute;left:90px;right:90px;top:230px;height:640px;border:3px solid var(--gold);background:#091522 url('{src}') center/cover no-repeat;box-shadow:0 20px 50px rgba(0,0,0,.4)}}
.pl-t{{position:absolute;left:100px;right:100px;top:920px;text-align:center;font-weight:400;font-size:66px;line-height:1.08;text-wrap:balance}}
.pl-c{{position:absolute;left:130px;right:130px;top:1090px;text-align:center;font-style:italic;font-size:32px;line-height:1.35;opacity:.92}}
"""
    body = (chrome() + f"<p class='eyebrow pl-eb'>{e(plate)}</p><div class='pl-img'></div>"
            f"<h1 class='pl-t'>{e(title)}</h1><p class='pl-c'>{e(caption)}</p>")
    return page(W, H, "navy", body, css)

def premise_card():
    css = """
.pm-arms{position:absolute;left:50%;top:140px;transform:translateX(-50%);width:600px}
.pm-eb{position:absolute;left:0;right:0;top:760px;text-align:center}
.pm-t{position:absolute;left:100px;right:100px;top:810px;text-align:center;font-weight:400;font-size:96px;line-height:1.04;letter-spacing:-.02em;text-wrap:balance}
.pm-t em{color:var(--crimson)}
.pm-s{position:absolute;left:150px;right:150px;top:1085px;text-align:center;font-size:34px;line-height:1.35;color:#2c3640}
"""
    body = (chrome() + f"<img class='pm-arms' src='{ASSETS}/royal-arms.svg' alt=''>"
        "<p class='eyebrow pm-eb'>Low Value Content presents</p>"
        "<h1 class='pm-t'>Official regalia for the <em>attention economy.</em></h1>"
        "<p class='pm-s'>Wearable observations on the systems, rituals, and small humiliations of online life.</p>")
    return page(W, H, "ivory", body, css)

def status_card():
    css = """
.s-eb{position:absolute;left:0;right:0;top:220px;text-align:center}
.s-mark{position:absolute;left:50%;top:290px;transform:translateX(-50%);width:130px}
.s-mid{position:absolute;left:110px;right:110px;top:460px;bottom:230px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.s-t{font-weight:400;font-size:92px;line-height:1.06;letter-spacing:-.02em;text-wrap:balance}
.s-p{margin-top:48px;max-width:820px;font-size:40px;line-height:1.42;color:#2c3640}
"""
    body = (chrome() + "<p class='eyebrow s-eb'>A note from the Chancery</p>"
        f"<img class='s-mark' src='{ASSETS}/royal-mark.svg' alt=''>"
        "<div class='s-mid'><h1 class='s-t'>In early product development.</h1>"
        "<p class='s-p'>The designs are working concepts, not products offered for sale. Final garments, colors, pricing, and availability depend on rights review, physical samples, and a successful test order.</p></div>")
    return page(W, H, "paper", body, css)

# ---------------------------------------------------------------- profile images
def avatar(size=1080):
    css = """
.av{position:absolute;inset:0;display:grid;place-items:center}
.av img{width:50%}
.ring{position:absolute;inset:9%;border-radius:50%;border:12px double var(--gold)}
"""
    body = f"<div class='ring'></div><div class='av'><img src='{ASSETS}/royal-mark.svg' alt=''></div>"
    return page(size, size, "navy", body, css)

def cover(w, h, tagline=True, scale=1.0):
    s = scale
    css = f"""
.cv{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:{int(34*s)}px}}
.cv img{{width:{int(150*s)}px;height:{int(150*s)}px}}
.cv .t b{{display:block;font-weight:400;font-size:{int(62*s)}px;letter-spacing:.1em;text-transform:uppercase;color:var(--ivory)}}
.cv .t i{{display:block;margin-top:{int(8*s)}px;font:{int(36*s)}px/1.1 var(--script);color:var(--gold-l)}}
.cv .t em{{display:block;margin-top:{int(20*s)}px;font:700 {int(16*s)}px/1 var(--sans);letter-spacing:.26em;text-transform:uppercase;color:rgba(244,238,223,.75);font-style:normal}}
.rule{{position:absolute;left:0;right:0;height:3px;background:var(--gold)}}
.rule.a{{top:{int(14*s)}px}}.rule.b{{bottom:{int(14*s)}px}}
"""
    tl = "<em>Official regalia for the attention economy</em>" if tagline else ""
    body = (f"<div class='rule a'></div><div class='rule b'></div><div class='cv'><img src='{ASSETS}/royal-mark.svg' alt=''>"
            f"<div class='t'><b>The Royal House of Engagement</b><i>Purveyed by Low Value Content</i>{tl}</div></div>")
    return page(w, h, "navy", body, css)
