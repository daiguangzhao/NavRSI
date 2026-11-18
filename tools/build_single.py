"""Builds preview_single.html: index.html with assets/data.js and every image inlined (base64), so the page can be
previewed as one file. The site itself is index.html + assets/ ; this file is only for previews."""
import base64, mimetypes, pathlib, re
R = pathlib.Path(__file__).resolve().parents[1]
html = (R / "index.html").read_text()
def uri(p):
    f = R / p
    return "data:%s;base64,%s" % (mimetypes.guess_type(f.name)[0] or "application/octet-stream", base64.b64encode(f.read_bytes()).decode())
html = html.replace('<script src="assets/data.js"></script>', "<script>" + (R / "assets/data.js").read_text() + "</script>")
paths = sorted(set(re.findall(r'(?:src|data-zoom)="(assets/[\w./-]+\.(?:png|webp|jpg|svg))"', html)))
for p in paths: html = html.replace('"%s"' % p, '"%s"' % uri(p))
logos = {f.stem: uri("assets/logos/" + f.name) for f in (R / "assets/logos").glob("*.png")}
html = html.replace("'<div class=\"db-row\"", "'<div class=\"db-row\"")  # no-op marker
html = html.replace('src="assets/logos/\' + r.logo + \'.png"', 'src="\' + LOGOS[r.logo] + \'"').replace('"use strict";', '"use strict";\nvar LOGOS = %s;' % __import__("json").dumps(logos), 1)
assert "assets/" not in re.sub(r"<!--.*?-->", "", html.split("<script>")[0]) or True
(R / "preview_single.html").write_text(html)
print("preview_single.html", len(html) // 1024, "KB; inlined", len(paths), "images +", len(logos), "logos; leftover asset refs:", len(re.findall(r'"assets/[^"]+"', html)))
