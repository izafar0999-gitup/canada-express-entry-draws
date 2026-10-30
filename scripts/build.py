#!/usr/bin/env python3
"""Build the Express Entry draws dataset from IRCC's official rounds JSON feed."""
import csv, json, re, sys, collections
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "raw" / "ee_rounds_123_en.json"
rounds = json.load(open(SRC, encoding="utf-8"))["rounds"]

def clean(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()
def num(s):
    s = clean(s).replace(",", "")
    return int(s) if s else None

PROGRAM = {
    "Provincial Nominee Program": "Provincial Nominee Program",
    "Canadian Experience Class": "Canadian Experience Class",
    "Federal Skilled Trades": "Federal Skilled Trades",
    "Federal Skilled Worker": "Federal Skilled Worker",
}
def classify(name):
    n = name.lower()
    if name in ("No Program Specified", "General"): return "General", "General (all programs)"
    if name in PROGRAM: return "Program-specific", PROGRAM[name]
    rules = [("french", "French language proficiency"),
             ("healthcare", "Healthcare and social services occupations"),
             ("physician", "Physicians with Canadian work experience"),
             ("senior manager", "Senior managers with Canadian work experience"),
             ("military", "Skilled military recruits"),
             ("stem", "STEM occupations"), ("trade", "Trade occupations"),
             ("transport", "Transport occupations"),
             ("agriculture", "Agriculture and agri-food occupations"),
             ("education", "Education occupations")]
    for k, v in rules:
        if k in n: return "Category-based", v
    raise SystemExit(f"Unclassified round name: {name!r}")

def tiebreak(s, draw_date=None, rnd=None):
    """IRCC tie-breaking timestamp -> ISO 8601. 'Z' only when IRCC states UTC."""
    s = clean(s)
    if not s: return ""
    utc = "UTC" in s
    t = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", s.replace("UTC", "")).replace(" at ", " ")
    if not re.search(r"\b(19|20)\d\d\b", t):  # IRCC omitted the year: use the draw's year (or the year before if that would postdate the draw)
        y = int(draw_date[:4]); t = re.sub(r"^(\w+ \d+)", lambda m: f"{m.group(1)} {y}", t.strip())
        d0 = datetime.strptime(re.sub(r"\s+", " ", t).split(" ")[0] + " " + re.sub(r"\s+", " ", t).split(" ")[1] + f" {y}", "%B %d %Y")
        if d0.strftime("%Y-%m-%d") > draw_date: t = t.replace(f" {y}", f" {y-1}", 1)
        INFERRED.append(rnd)
    t = re.sub(r"\s+", " ", re.sub(r"(\d)\.\s", r"\1 ", t).replace(",", " ")).strip()
    for fmt in ("%B %d %Y %H:%M:%S", "%B %d %Y %I:%M:%S %p", "%B %d %Y %H:%M", "%b %d %Y %H:%M:%S", "%B %d %Y %H:%M:%S %p"):
        try:
            d = datetime.strptime(t, fmt)
            return d.strftime("%Y-%m-%dT%H:%M:%S") + ("Z" if utc else "")
        except ValueError: pass
    BAD.append(s); return s

def sortkey(x):
    m = re.match(r"(\d+)([a-z]?)", x["round_number"]); return (x["date"], int(m.group(1)), m.group(2))

rows, dist, BAD, MISMATCH, INFERRED = [], [], [], [], []
BINS = ["601_1200","501_600","451_500","491_500","481_490","471_480","461_470","451_460",
        "401_450","441_450","431_440","421_430","411_420","401_410","351_400","301_350","0_300","total"]
for r in rounds:
    name = clean(r["drawName"]); rtype, cat = classify(name)
    row = dict(round_number=clean(r["drawNumber"]), date=clean(r["drawDate"]),
               round_type=rtype, category=cat, invitations=num(r["drawSize"]),
               crs_cutoff=num(r["drawCRS"]), tie_breaking_rule=tiebreak(r["drawCutOff"], clean(r["drawDate"]), clean(r["drawNumber"])),
               ircc_round_name=name, eligible_programs=clean(r["drawText2"]))
    datetime.strptime(row["date"], "%Y-%m-%d")
    rows.append(row)
    dd = [num(r[f"dd{i}"]) for i in range(1, 19)]
    if dd[17]:
        # IRCC sub-bins should add up to their parent bins and the total; flag (not fix) any that don't
        ok = (sum(dd[3:8]) == dd[2] and sum(dd[9:14]) == dd[8]
              and dd[0]+dd[1]+dd[2]+dd[8]+dd[14]+dd[15]+dd[16] == dd[17])
        if not ok: MISMATCH.append(row["round_number"])
        d = dict(round_number=row["round_number"], date=row["date"],
                 distribution_as_of=datetime.strptime(clean(r["drawDistributionAsOn"]), "%B %d, %Y").strftime("%Y-%m-%d"))
        d.update({f"candidates_{b}": v for b, v in zip(BINS, dd)}); d["bins_add_up"] = "yes" if ok else "no"
        dist.append(d)

if BAD: raise SystemExit("Unparsed: " + repr(BAD))
rows.sort(key=sortkey, reverse=True); dist.sort(key=sortkey, reverse=True)
cols = list(rows[0].keys())
def write(path, data, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(data)
write(ROOT/"express_entry_draws.csv", rows, cols)
y26 = [x for x in rows if x["date"].startswith("2026")]
write(ROOT/"express_entry_draws_2026.csv", y26, cols)
write(ROOT/"express_entry_crs_score_distribution.csv", dist, list(dist[0].keys()))

# stats
st = {"total_rounds": len(rows), "first": rows[-1], "latest": rows[0], "rows_2026": len(y26),
      "distribution_rows": len(dist), "distribution_mismatch_rounds": MISMATCH, "tiebreak_year_inferred": INFERRED, "invitations_2026": sum(x["invitations"] for x in y26),
      "invitations_all": sum(x["invitations"] for x in rows), "by_cat_2026": {}}
g = collections.defaultdict(list)
for x in y26: g[x["category"]].append(x)
for c, xs in sorted(g.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    cut = [x["crs_cutoff"] for x in xs]
    st["by_cat_2026"][c] = dict(rounds=len(xs), invitations=sum(x["invitations"] for x in xs), min=min(cut), max=max(cut))
st["by_type_2026"] = dict(collections.Counter(x["round_type"] for x in y26))
json.dump(st, open(ROOT/"scripts"/"stats.json", "w"), indent=1, default=str)
print(json.dumps(st, indent=1, default=str))
