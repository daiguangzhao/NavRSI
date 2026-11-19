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
- The opening: the page's text rises in first, and the particles arrive as a swirling cloud that brightens as each
  one lands in the word. `MIST` in `index.html` sets how bright the waiting cloud is, what share of it is lit, and
  how strong its streaks are; `OPEN` holds its duration and flow.
- Without WebGL the page falls back to a Canvas 2D version (5,200 particles, three shapes).
- `prefers-reduced-motion` shows one still frame and stops every animation.
- URL switches for checking: `?nogl=1` forces the fallback, `?hq=1` locks the top quality level, and `?herodebug=1`
  exposes `window.__navrsiHero.show(to, from, progress, time)` to hold one moment still (`from = 4` is the opening
  cloud).

## The foil sweep on the rest of the page

The light that sweeps over the hero's shapes returns further down as a band of light carrying glitter:

- Cards, headings and the closing statement: the band crosses each of them once when they come into view. Under the
  cursor a card shows the same glitter.
- Gradient text and the headline numbers get a narrow sheen, the figures a pale band of coloured light.
- The brand in the navigation bar repeats the hero's two lights at the hero's pace: the golden pulse over the five
  figures and the diagonal sweep over the name.

The glitter is one 480 px tile drawn by the script at load and handed to the CSS as `--glit`.

## Credits

Vendor icons are from LobeHub Icons (`@lobehub/icons-static-png`, MIT). The logos are trademarks of their owners and
only mark which model family a row shows.
