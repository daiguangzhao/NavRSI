# NavRSI project page

Source of the project page of **NavRSI: Recursive Harness Self-Improvement for Vision-and-Language Navigation**.

Live page: https://daiguangzhao.github.io/NavRSI/

The paper and the source code will be linked from the page once they are released.

## About this repository

A static site: `index.html` and `assets/`, with no build step and no framework. The only outside request is Google Fonts.

- `assets/data.js` holds the numbers behind the interactive charts. It is generated from the paper's table sources by
  `tools/extract_data.py`.
- `assets/*.webp` are the paper's figures.
- `tools/build_single.py` writes `preview_single.html`, a one-file copy with everything inlined, for offline previews.

## Hero particles

- WebGL: 42,000 particles on a desktop (26,000 on tablets, 15,000 on phones) morph between four shapes: the word,
  the five-stage strip of the title logo, a flowing 3D infinity loop and the headline number. Depth of field, streaks
  during the morphs, pointer tilt and repulsion, a shockwave on click, and a dissolve on scroll are all computed in
  the vertex shader. A governor lowers the pixel ratio and then the particle count on a slow device.
- Without WebGL the page falls back to a Canvas 2D version (5,200 particles, three shapes).
- `prefers-reduced-motion` shows one still frame and stops every animation.
- URL switches for checking: `?nogl=1` forces the fallback, `?hq=1` locks the top quality level, and `?herodebug=1`
  exposes `window.__navrsiHero.show(to, from, progress, time)` to hold one moment still.

## Credits

Vendor icons are from LobeHub Icons (`@lobehub/icons-static-png`, MIT). The logos are trademarks of their owners and
only mark which model family a row shows.
