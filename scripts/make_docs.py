#!/usr/bin/env python3
import json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
st = json.load(open(ROOT/"scripts"/"stats.json"))
L = st["latest"]; F = st["first"]
SRC = "https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json"
PAGE = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations.html"
OGL = "https://open.canada.ca/en/open-government-licence-canada"
TITLE = "Canada Express Entry Draws Dataset (CRS Cut-offs and Invitations)"
def n(x): return f"{x:,}"

cat_rows = "\n".join(f"| {c} | {v['rounds']} | {n(v['invitations'])} | {v['min']} | {v['max']} |" for c, v in st["by_cat_2026"].items())
types = ", ".join(f"{k}: {v}" for k, v in st["by_type_2026"].items())

readme = f"""# {TITLE}

Every Canada Express Entry round of invitations (draw) published by Immigration, Refugees and Citizenship Canada (IRCC), from round #1 on {F['date']} to round #{L['round_number']} on {L['date']}, in clean, analysis-ready CSV files. Each row gives the round number, date, round type, category, number of invitations to apply (ITAs) issued, the CRS score of the lowest-ranked candidate invited (the cut-off) and the tie-breaking rule. A separate file contains the CRS score distribution of the Express Entry pool that IRCC published with each round.

Use it to chart CRS cut-off trends, compare category-based draws (French, healthcare, trades, STEM and others) with Canadian Experience Class and Provincial Nominee Program draws, or estimate your chances in the next draw. To check your own score, use the free CRS calculator at https://crscalcu.ca/.

**Last updated:** October 30, 2026, through round #{L['round_number']} ({L['date']}, {L['ircc_round_name']}, {n(L['invitations'])} invitations, CRS cut-off {L['crs_cutoff']}).

**Maintained by [crscalcu.ca](https://crscalcu.ca/)**, the [free CRS calculator](https://crscalcu.ca/) for Express Entry. For a readable table of recent rounds with analysis, see [Latest Express Entry draws and CRS cut-offs](https://crscalcu.ca/latest-express-entry-draws-crs-cutoffs/).

## Files

| File | Rows | Contents |
| --- | --- | --- |
| express_entry_draws.csv | {st['total_rounds']} | All rounds of invitations, {F['date'][:4]} to {L['date'][:4]}, newest first |
| express_entry_draws_2026.csv | {st['rows_2026']} | Rounds held in 2026 only, same columns |
| express_entry_crs_score_distribution.csv | {st['distribution_rows']} | CRS score distribution of the pool published with each round (rounds where IRCC published one) |

## Columns: express_entry_draws.csv and express_entry_draws_2026.csv

| Column | Type | Description |
| --- | --- | --- |
| round_number | text | IRCC round number. Text because IRCC numbered two same-day rounds 91a and 91b (May 30, 2018). |
| date | date (YYYY-MM-DD) | Date of the round. |
| round_type | text | IRCC round type: General, Program-specific or Category-based. |
| category | text | Normalized program or category, for example Canadian Experience Class, Provincial Nominee Program, French language proficiency, Healthcare and social services occupations. Early rounds IRCC labelled "No Program Specified" and later "General" rounds are both mapped to General (all programs). Category versions (Version 1, 2026-Version 2 and so on) are merged into one category name; the exact IRCC name is kept in ircc_round_name. |
| invitations | integer | Number of invitations to apply issued in the round. |
| crs_cutoff | integer | CRS score of the lowest-ranked candidate invited. |
| tie_breaking_rule | datetime (ISO 8601) | Tie-breaking rule: candidates with the cut-off score who submitted their Express Entry profile before this date and time were invited. A trailing Z means IRCC stated the time in UTC. Empty where IRCC published no tie-breaking rule (mostly early rounds). |
| ircc_round_name | text | Round name exactly as published by IRCC. |
| eligible_programs | text | Programs included in the round, as published by IRCC. |

## Columns: express_entry_crs_score_distribution.csv

round_number, date and distribution_as_of (the date of the pool snapshot IRCC published with the round), followed by the number of candidates in each CRS score range: candidates_601_1200, candidates_501_600, candidates_451_500 (broken down into candidates_491_500, candidates_481_490, candidates_471_480, candidates_461_470, candidates_451_460), candidates_401_450 (broken down into candidates_441_450, candidates_431_440, candidates_421_430, candidates_411_420, candidates_401_410), candidates_351_400, candidates_301_350, candidates_0_300 and candidates_total. The column bins_add_up is "yes" when the sub-ranges add up to their parent ranges and the total. IRCC's published figures are kept unchanged; the only round where they do not add up is #{', #'.join(st['distribution_mismatch_rounds']) or 'none'}. IRCC published the same snapshot for several rounds held in the same week, so consecutive rows can repeat.

## 2026 summary

These figures are computed directly from express_entry_draws_2026.csv (rounds held January 1 to {L['date']}, 2026).

- Rounds in 2026: {st['rows_2026']} ({types})
- Total invitations issued in 2026: {n(st['invitations_2026'])}
- Total invitations across all {st['total_rounds']} rounds since {F['date'][:4]}: {n(st['invitations_all'])}

| Category (2026) | Rounds | Invitations | Lowest CRS cut-off | Highest CRS cut-off |
| --- | --- | --- | --- | --- |
{cat_rows}

## Source and licence

All figures come from Immigration, Refugees and Citizenship Canada's official rounds of invitations data feed, {SRC}, which powers the Rounds of invitations page at {PAGE}. Data retrieved October 30, 2026.

Contains information licensed under the Open Government Licence – Canada ({OGL}).

The compilation (cleaning, normalized categories, ISO dates and documentation) is released by crscalcu.ca under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). See the LICENSE file. crscalcu.ca is an independent site and is not affiliated with or endorsed by IRCC or the Government of Canada. Always confirm details on canada.ca before making immigration decisions.

## Processing notes

- Numbers were stripped of thousands separators; HTML was removed from text fields.
- Tie-breaking timestamps published in mixed formats (for example "August 31st, 2026 at 10:42:13 UTC") were converted to ISO 8601. For round #{', #'.join(st['tiebreak_year_inferred'])}, IRCC omitted the year ("October 7 at 16:38:21 UTC"), so the year of the round was used.
- No rows were added, removed or corrected. 2026 rows were cross-checked against crscalcu.ca's independently verified draw table with no differences.
- scripts/build.py rebuilds every file from the IRCC JSON.

## How to cite

crscalcu.ca (2026). {TITLE}. Data from Immigration, Refugees and Citizenship Canada, Open Government Licence – Canada. Updated October 30, 2026, through round #{L['round_number']}. https://crscalcu.ca/latest-express-entry-draws-crs-cutoffs/

Please link to https://crscalcu.ca/ when you use or republish this data.
"""
(ROOT/"README.md").write_text(readme, encoding="utf-8")

lic = f"""Canada Express Entry Draws Dataset (CRS Cut-offs and Invitations)
Maintained by crscalcu.ca (https://crscalcu.ca/)

1. Source data

The underlying data (round numbers, dates, round names, invitations, CRS cut-offs,
tie-breaking rules and CRS score distributions) is published by Immigration,
Refugees and Citizenship Canada (IRCC) at
{SRC}
and is used under the Open Government Licence – Canada:
{OGL}

Contains information licensed under the Open Government Licence – Canada.

2. Compilation

The compilation, cleaning, normalized fields, file structure, scripts and
documentation are Copyright (c) 2026 crscalcu.ca and are licensed under the
Creative Commons Attribution 4.0 International licence (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/

You are free to share and adapt this material for any purpose, including
commercially, provided you give appropriate credit to crscalcu.ca with a link to
https://crscalcu.ca/, indicate if changes were made, and also keep the IRCC
attribution required by the Open Government Licence – Canada.

3. No endorsement

crscalcu.ca is not affiliated with or endorsed by IRCC or the Government of
Canada. The data is provided as is, without warranty of any kind.
"""
(ROOT/"LICENSE").write_text(lic, encoding="utf-8")

K = ROOT/"kaggle"; K.mkdir(exist_ok=True)
def fields(names, desc):
    return [{"name": c, "description": desc.get(c, "")} for c in names]
d1 = {"round_number": "IRCC round number (text; includes 91a and 91b)", "date": "Round date, YYYY-MM-DD",
      "round_type": "General, Program-specific or Category-based", "category": "Normalized program or category",
      "invitations": "Invitations to apply issued", "crs_cutoff": "CRS score of the lowest-ranked candidate invited",
      "tie_breaking_rule": "Tie-breaking date and time, ISO 8601 (Z = UTC)", "ircc_round_name": "Round name as published by IRCC",
      "eligible_programs": "Programs included in the round, as published by IRCC"}
import csv
hdr = lambda f: next(csv.reader(open(ROOT/f)))
meta = {
  "title": "Canada Express Entry Draws (CRS Cut-offs)",
  "id": "izafar0999/canada-express-entry-draws",
  "subtitle": f"All IRCC Express Entry rounds 2015-2026: CRS cut-offs, ITAs, categories",
  "description": readme,
  "isPrivate": False,
  "licenses": [{"name": "CC-BY-4.0"}],
  "keywords": ["canada", "immigration", "government", "demographics"],
  "resources": [
    {"path": "express_entry_draws.csv", "description": "All Express Entry rounds of invitations", "schema": {"fields": fields(hdr("express_entry_draws.csv"), d1)}},
    {"path": "express_entry_draws_2026.csv", "description": "Express Entry rounds held in 2026", "schema": {"fields": fields(hdr("express_entry_draws_2026.csv"), d1)}},
    {"path": "express_entry_crs_score_distribution.csv", "description": "CRS score distribution of the pool published with each round", "schema": {"fields": fields(hdr("express_entry_crs_score_distribution.csv"), {})}},
  ],
}
assert len(meta["title"]) <= 50 and 20 <= len(meta["subtitle"]) <= 80, (len(meta["title"]), len(meta["subtitle"]))
json.dump(meta, open(K/"dataset-metadata.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
for f in ["express_entry_draws.csv", "express_entry_draws_2026.csv", "express_entry_crs_score_distribution.csv"]:
    shutil.copy(ROOT/f, K/f)
print("ok", len(meta["title"]), len(meta["subtitle"]))
