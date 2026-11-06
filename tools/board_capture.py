"""Capture an animated canvas board (a Design-canvas .dc.html) as RGBA frames at exact times, in headless Chromium.
For boards whose motion is CSS (Kit's V3.00 scenes: parallax translateX steps; prop sheets: per-frame opacity keyframes).
Every CSS animation is paused and seeked to t, so a frame is exactly what the board shows at t. Pixel art stays crisp:
the svg is drawn at a whole-number scale with crispEdges, then the PNG is the true grid (scale 1) or k-times it.

    from board_capture import capture
    ims = capture("SCN17V3_00.dc.html", "Riding in a car", times=[i / 10 for i in range(30)], scale=1)
Renders stay out of git (callers cache under their own out dir)."""
import io, os
from PIL import Image
from playwright.sync_api import sync_playwright

JS_SEEK = """t => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; } }"""

def capture(html_path, label_prefix, times, scale=1, transparent=True):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 2000})
        pg.goto("file://" + os.path.abspath(html_path)); pg.wait_for_timeout(200)
        nth = 0
        if "#" in label_prefix: label_prefix, nth = label_prefix.rsplit("#", 1); nth = int(nth) - 1   # "Label#2" = the 2nd board with that label
        sel = f'svg[aria-label^="{label_prefix}"]'
        els = pg.query_selector_all(sel); el = els[nth] if len(els) > nth else None
        if el is not None and nth:
            pg.evaluate("([s, n]) => { document.querySelectorAll(s).forEach((e, i) => { if (i !== n) e.removeAttribute('aria-label'); }); }", [sel, nth]); sel = f'svg[aria-label^="{label_prefix}"]'
        if el is None: raise KeyError(f"no svg labelled {label_prefix!r} in {html_path}")
        vb = [float(v) for v in el.get_attribute("viewBox").split()]
        w, h = int(vb[2] * scale), int(vb[3] * scale)
        pg.evaluate("""([s, w, h]) => { const e = document.querySelector(s); e.setAttribute('width', w); e.setAttribute('height', h);
            e.style.display = 'block'; document.body.style.background = 'transparent';
            let n = e.parentElement; while (n) { if (n.style) { n.style.background = 'transparent'; n.style.outline = 'none'; } n = n.parentElement; } }""", [sel, w, h])
        out = []
        for t in times:
            pg.evaluate(JS_SEEK, t)
            png = el.screenshot(omit_background=transparent, animations="allow")
            out.append(Image.open(io.BytesIO(png)).convert("RGBA").resize((w, h), Image.NEAREST))
        b.close()
    return out

def durations(html_path):
    """Loop lengths (s) of the board's CSS animations, longest first."""
    import re
    css = open(html_path, encoding="utf-8").read()
    return sorted({float(d) for d in re.findall(r'animation:\S+ ([\d.]+)s', css)}, reverse=True)
