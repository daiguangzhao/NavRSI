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
  how strong its streaks are; `OPEN` holds its duration and flow. The hero keeps this stage to itself: the foil wall
  below starts where the hero ends.
- Without WebGL the page falls back to a Canvas 2D version (5,200 particles, three shapes).
- `prefers-reduced-motion` shows one still frame and stops every animation.

## The foil wall behind the page

Below the hero, the opening's shapes return in small as a watermark behind the whole page (windows 760 px wide or
more, WebGL only):

- One unit is one whole shape, and every unit shows the same kind at the same time: the name, the whole five-stage
  strip, the infinity loop, or the headline number. The wall follows the hero's cycle while the hero runs and keeps
  the same cycle on its own further down; all units change together, in a wave from the middle outwards.
- The units lean to the right like cards on a slope, in close rows with every other row half a step across. They
  lie behind everything, a little brighter in the page's margins than behind the text (`CENTER`, `EDGE`, `LEAN`).
- One light for the whole wall: a band of colour flows across it and every unit takes the colour of its place, the
  wall breathes together, a crest of light runs through the units in order, and each unit's own light (the golden
  pulse over the strip, the diagonal sweep over the name and the number, the comets round the loop) runs in step.
- Panels have dark glass under them and free text has a dark edge (`--glass`, `--halo`), so both stay readable.

## The sweep and the sheen

- Now and then, and whenever a new section heading comes into view, one band of light crosses the page. The foil
  wall flares where it passes, the stars in it flare, and the glitter of the star field lights up under it.
- Cards, headings and the closing statement: a band of glitter crosses each of them once when they come into view.
  Under the cursor a card shows the same glitter (one 480 px tile drawn by the script, handed to the CSS as `--glit`).
- Gradient text and the headline numbers get a narrow sheen, the figures a pale band of coloured light.
- The brand in the navigation bar repeats the hero's two lights at the hero's pace: the golden pulse over the five
  figures and the diagonal sweep over the name.

## Switches for checking

- `?nogl=1` forces the Canvas 2D hero, `?hq=1` locks the top quality level (hero and wall).
- `?herodebug=1` exposes `window.__navrsiHero.show(to, from, progress, time)` to hold one moment of the hero still
  (`from = 4` is the opening cloud), `window.__navrsiWall.show(kind, from, progress, time)` to hold the wall
  (kinds: 0 the name, 1 the strip, 2 the loop, 3 the number), and `window.__navrsiSky(k)` to hold the page-wide
  sweep at the fraction `k` of its way.

## Credits

Vendor icons are from LobeHub Icons (`@lobehub/icons-static-png`, MIT). The logos are trademarks of their owners and
only mark which model family a row shows.
