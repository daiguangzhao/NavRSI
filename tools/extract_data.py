"""Reads the paper's table sources (paper/navrsi_arxiv/tables) and writes assets/data.js for the project page.
Every number on the page that comes from a table is taken from here, never typed by hand."""
import json, re, pathlib
A = pathlib.Path(__file__).resolve().parents[2] / "navrsi_arxiv/tables"
OUT = pathlib.Path(__file__).resolve().parents[1] / "assets/data.js"
def clean(s):
    s = re.sub(r"\\cellcolor\[rgb\]\{[^}]*\}", "", s)
    s = re.sub(r"\\cite\{[^}]*\}", "", s)
    s = re.sub(r"\\kern-?[0-9.]+em", "", s)
    s = re.sub(r"\\harnessicon\{[^}]*\}", "", s)
    return s
def num(cell):
    cell = re.sub(r"\\mc\{\d+\}\{(.*)\}\s*$", r"\1", cell.strip())
    cell = cell.replace("\\textbf{", "").replace("}", " ").replace("{", " ")
    m = re.search(r"-?\d+(?:\.\d+)?", cell)
    sd = re.search(r"\\pm\$?\s*([0-9.]+)", cell)
    return (float(m.group()) if m else None, float(sd.group(1)) if sd else None)
VENDOR = {"Claude Agent SDK": "Anthropic", "Codex CLI": "OpenAI", "Antigravity": "Google", "Qwen Code": "Alibaba"}
LOGO = {"Anthropic": "claude-color", "OpenAI": "openai", "Google": "gemini-color", "Alibaba": "qwen-color"}
native, rows = [], []
for line in (A / "r2r_native_compare.tex").read_text().splitlines():
    if line.startswith("%") or line.count("&") != 10 or "rowcolor" in line: continue
    c = [x.strip() for x in clean(line).rstrip("\\ ").split("&")]
    rows.append(c)
for a, b in zip(rows[0::2], rows[1::2]):
    assert "NavRSI" in b[0] and a[1] == b[1], (a[:2], b[:2])
    keys = ["ne", "osr", "sr", "spl", "turns", "cost", "tokens", "tokens_sr", "cost_sr"]
    native.append({"llm": a[1], "harness": a[0], "vendor": VENDOR[a[0]], "logo": LOGO[VENDOR[a[0]]],
                   "native": {k: num(v)[0] for k, v in zip(keys, a[2:])}, "native_sd": {k: num(v)[1] for k, v in zip(keys[:4], a[2:6])},
                   "ours": {k: num(v)[0] for k, v in zip(keys, b[2:])}, "ours_sd": {k: num(v)[1] for k, v in zip(keys[:4], b[2:6])}})
sota = []
for line in (A / "full_split_compare.tex").read_text().splitlines():
    s = line.strip()
    if s.startswith("%") or s.count("&") != 13 or "rowcolor" in s: continue
    c = [x.strip() for x in clean(s).rstrip("\\ ").split("&")]
    name = re.sub(r"~?\\flame|\\textsc\{|\\textbf\{|[{}~]", "", c[0]).replace("\\flame", "").strip()
    name = re.sub(r"\s+", " ", name)
    sota.append({"method": name, "trained": "\\flame" in c[0], "single_rgb": "checkmark" in c[4], "external": re.sub(r"\\textbf\{|\}", "", c[5]),
                 "r2r": {k: num(v)[0] for k, v in zip(["ne", "osr", "sr", "spl"], c[6:10])},
                 "rxr": {k: num(v)[0] for k, v in zip(["ne", "ndtw", "sr", "spl"], c[10:14])}})
real = []
for line in (A / "realworld_compare.tex").read_text().splitlines():
    if "GPT-6-Astra" in line and line.count("&") == 3:
        c = [x.strip() for x in clean(line).rstrip("\\ ").split("&")]
        name = re.sub(r"\\textsc\{|\\textbf\{|[{}~]|\(GPT-6-Astra\)|\(ours\)", "", c[0]).strip()
        real.append({"method": name, "ne": num(c[1])[0], "osr": num(c[2])[0], "sr": num(c[3])[0]})
seed, srows = [], []
for line in (A / "r2r_mip_compare.tex").read_text().splitlines():
    if line.startswith("%") or line.count("&") != 6 or "rowcolor" in line: continue
    srows.append([x.strip() for x in clean(line).rstrip("\\ ").split("&")])
for a, b in zip(srows[0::2], srows[1::2]):
    assert a[0] == "Seed 0" and "NavRSI" in b[0] and a[1] == b[1], (a[:2], b[:2])
    seed.append({"llm": a[1], "seed": num(a[2])[0], "ours": num(b[2])[0]})
# rows measured after the paper (tools/extra_native.json), placed after the last row of the same native harness
extra = json.loads((pathlib.Path(__file__).resolve().parent / "extra_native.json").read_text())
for x in extra:
    have = [r for r in native if r["llm"] == x["llm"]]
    if have:  # the row is in the paper's table by now: keep the table's numbers, only mark it as new
        have[0]["extra"] = True; have[0]["note"] = x["note"]; continue
    last = max(i for i, r in enumerate(native) if r["harness"] == x["harness"])
    native.insert(last + 1, x)
gains = [round(r["ours"]["sr"] - r["native"]["sr"], 1) for r in native]
gpt4 = [r for r in native if not r.get("extra") and r["llm"] in ("gpt-6-luna", "gpt-6.1-terra", "gpt-6.1-sol", "gpt-6-astra")]
derived = {"n_llms": len(native), "n_vendors": len({r["vendor"] for r in native}), "n_improved_sr": sum(g > 0 for g in gains),
           "max_gain": max(gains), "max_gain_llm": native[gains.index(max(gains))]["llm"],
           "codex_cost_native": round(sum(r["native"]["cost"] for r in gpt4) / 4, 4), "codex_cost_ours": round(sum(r["ours"]["cost"] for r in gpt4) / 4, 4)}
derived["codex_cost_drop_pct"] = round(100 * (1 - derived["codex_cost_ours"] / derived["codex_cost_native"]), 1)
data = {"native": native, "sota": sota, "real": real, "seed": seed, "derived": derived}
OUT.write_text("window.NAVRSI_DATA = " + json.dumps(data, indent=1) + ";\n")
print(json.dumps(derived)); print(len(native), "LLM pairs;", len(sota), "full-split rows;", real)
print([(r["llm"], r["native"]["sr"], r["ours"]["sr"]) for r in native])
print([(r["method"], r["r2r"]["sr"], r["rxr"]["sr"]) for r in sota]); print(seed)
