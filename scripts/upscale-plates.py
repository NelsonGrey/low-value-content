#!/usr/bin/env python3
"""Upscale the ornate artwork plates (Nos. 07-10) to print resolution.

    python3 scripts/upscale-plates.py WEIGHTS.pth OUT_DIR [A07 A08 ...]   # step 1: AI upscale (about 8 min per plate on 2 CPUs)
    python3 scripts/upscale-plates.py finalize OUT_DIR FINAL_DIR          # step 2: blend and size the print file

Step 1 runs Real-ESRGAN x4plus (BSD-3) tiled on CPU and fits the result to a
4500 x 5400 px transparent canvas. Step 2 produces the print file: the art at
3600 x 4500 px (12 x 15 in at 300 dpi, a standard chest print), blending 60%
AI upscale with 40% plain Lanczos resample of the original plate. The AI pass
gives crisp contours but adds painterly artefacts in fine texture; the plain
resample is clean but soft; the blend keeps the edges and calms the texture.
Needs torch, numpy, Pillow and opencv. Weights: RealESRGAN_x4plus.pth (not in the repo).
Output is a candidate print file: it still needs a sample print and a visual check.
"""
import sys, glob, time
from pathlib import Path
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, cv2
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "mockups" / "royal-house"
W, H = 4500, 5400

class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__()
        s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1); s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1); s.lrelu = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        x1 = s.lrelu(s.conv1(x)); x2 = s.lrelu(s.conv2(torch.cat((x, x1), 1)))
        x3 = s.lrelu(s.conv3(torch.cat((x, x1, x2), 1))); x4 = s.lrelu(s.conv4(torch.cat((x, x1, x2, x3), 1)))
        return s.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x

class RRDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__(); s.rdb1 = RDB(nf, gc); s.rdb2 = RDB(nf, gc); s.rdb3 = RDB(nf, gc)
    def forward(s, x): return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x

class RRDBNet(nn.Module):
    def __init__(s, nf=64, nb=23, gc=32):
        super().__init__()
        s.conv_first = nn.Conv2d(3, nf, 3, 1, 1); s.body = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
        s.conv_body = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_last = nn.Conv2d(nf, 3, 3, 1, 1); s.lrelu = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        f = s.conv_first(x); f = f + s.conv_body(s.body(f))
        f = s.lrelu(s.conv_up1(F.interpolate(f, scale_factor=2, mode="nearest")))
        f = s.lrelu(s.conv_up2(F.interpolate(f, scale_factor=2, mode="nearest")))
        return s.conv_last(s.lrelu(s.conv_hr(f)))

def load(weights):
    net = RRDBNet(); sd = torch.load(weights, map_location="cpu")
    net.load_state_dict(sd.get("params_ema", sd.get("params", sd)), strict=True); return net.eval()

@torch.no_grad()
def upscale4(net, rgb, tile=192, pad=16):
    h, w, _ = rgb.shape
    t = torch.from_numpy(rgb.astype(np.float32) / 255).permute(2, 0, 1)[None]
    out = torch.zeros(1, 3, h * 4, w * 4)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            y0, x0 = max(y - pad, 0), max(x - pad, 0); y1, x1 = min(y + tile + pad, h), min(x + tile + pad, w)
            o = net(t[:, :, y0:y1, x0:x1])
            ys, xs = (y - y0) * 4, (x - x0) * 4
            th, tw = min(tile, h - y), min(tile, w - x)
            out[:, :, y * 4:(y + th) * 4, x * 4:(x + tw) * 4] = o[:, :, ys:ys + th * 4, xs:xs + tw * 4]
    return (out.clamp(0, 1)[0].permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)

def run(net, path, outdir):
    im = np.array(Image.open(path).convert("RGBA")); rgb, a = im[..., :3].copy(), im[..., 3]
    # Fill transparent pixels with nearby colour so the model does not invent dark halos.
    mask = (a < 8).astype(np.uint8) * 255
    rgb = cv2.inpaint(rgb, mask, 5, cv2.INPAINT_TELEA)
    up = upscale4(net, rgb)
    a4 = cv2.resize(a, (a.shape[1] * 4, a.shape[0] * 4), interpolation=cv2.INTER_CUBIC)
    out = Image.fromarray(np.dstack([up, a4]), "RGBA")
    scale = min(W / out.width, H / out.height)
    out = out.resize((round(out.width * scale), round(out.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0)); canvas.alpha_composite(out, ((W - out.width) // 2, (H - out.height) // 2))
    dest = Path(outdir) / (Path(path).stem + "-print.png"); canvas.save(dest, dpi=(300, 300), optimize=True); return dest

def finalize(indir, outdir, ai=0.6):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(indir).glob("A*-print.png")):
        src = next(SRC.glob(f.name.replace("-print.png", ".png")))
        up = Image.open(f).convert("RGBA")
        art = up.crop((90, 0, 4410, 5400)).resize((3600, 4500), Image.LANCZOS)  # drop transparent side margins
        plain = Image.open(src).convert("RGBA").resize((3600, 4500), Image.LANCZOS)
        a = np.asarray(art, dtype=np.float32); b = np.asarray(plain, dtype=np.float32)
        out = a * ai + b * (1 - ai); out[..., 3] = a[..., 3]
        dest = Path(outdir) / f.name.replace("-print.png", "-3600x4500.png")
        Image.fromarray(out.round().astype(np.uint8), "RGBA").save(dest, dpi=(300, 300), optimize=True); print(dest)

if __name__ == "__main__":
    if sys.argv[1] == "finalize":
        finalize(sys.argv[2], sys.argv[3]); sys.exit(0)
    weights, outdir, *keys = sys.argv[1:]
    torch.set_num_threads(max(1, torch.get_num_threads()))
    net = load(weights); Path(outdir).mkdir(parents=True, exist_ok=True)
    files = sorted(SRC.glob("A*.png")) if not keys else [f for k in keys for f in SRC.glob(f"{k}-*.png")]
    for f in files:
        t = time.time(); print(run(net, f, outdir), f"{time.time() - t:.0f}s", flush=True)
