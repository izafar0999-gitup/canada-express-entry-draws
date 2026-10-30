# Canada Express Entry Draws Dataset (CRS Cut-offs and Invitations)

Every Canada Express Entry round of invitations (draw) published by Immigration, Refugees and Citizenship Canada (IRCC), from round #1 on 2015-01-31 to round #453 on 2026-10-28, in clean, analysis-ready CSV files. Each row gives the round number, date, round type, category, number of invitations to apply (ITAs) issued, the CRS score of the lowest-ranked candidate invited (the cut-off) and the tie-breaking rule. A separate file contains the CRS score distribution of the Express Entry pool that IRCC published with each round.

Use it to chart CRS cut-off trends, compare category-based draws (French, healthcare, trades, STEM and others) with Canadian Experience Class and Provincial Nominee Program draws, or estimate your chances in the next draw. To check your own score, use the free CRS calculator at https://crscalcu.ca/.

**Last updated:** October 30, 2026, through round #453 (2026-10-28, Transport Occupations, 2026-Version 2, 150 invitations, CRS cut-off 477).

**Maintained by [crscalcu.ca](https://crscalcu.ca/)**, the [free CRS calculator](https://crscalcu.ca/) for Express Entry. For a readable table of recent rounds with analysis, see [Latest Express Entry draws and CRS cut-offs](https://crscalcu.ca/latest-express-entry-draws-crs-cutoffs/).

## Files

| File | Rows | Contents |
| --- | --- | --- |
| express_entry_draws.csv | 454 | All rounds of invitations, 2015 to 2026, newest first |
| express_entry_draws_2026.csv | 65 | Rounds held in 2026 only, same columns |
| express_entry_crs_score_distribution.csv | 236 | CRS score distribution of the pool published with each round (rounds where IRCC published one) |

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

round_number, date and distribution_as_of (the date of the pool snapshot IRCC published with the round), followed by the number of candidates in each CRS score range: candidates_601_1200, candidates_501_600, candidates_451_500 (broken down into candidates_491_500, candidates_481_490, candidates_471_480, candidates_461_470, candidates_451_460), candidates_401_450 (broken down into candidates_441_450, candidates_431_440, candidates_421_430, candidates_411_420, candidates_401_410), candidates_351_400, candidates_301_350, candidates_0_300 and candidates_total. The column bins_add_up is "yes" when the sub-ranges add up to their parent ranges and the total. IRCC's published figures are kept unchanged; the only round where they do not add up is #247. IRCC published the same snapshot for several rounds held in the same week, so consecutive rows can repeat.

## 2026 summary

These figures are computed directly from express_entry_draws_2026.csv (rounds held January 1 to 2026-10-28, 2026).

- Rounds in 2026: 65 (Category-based: 26, Program-specific: 39)
- Total invitations issued in 2026: 149,409
- Total invitations across all 454 rounds since 2015: 1,066,657

| Category (2026) | Rounds | Invitations | Lowest CRS cut-off | Highest CRS cut-off |
| --- | --- | --- | --- | --- |
| Provincial Nominee Program | 21 | 10,814 | 697 | 805 |
| Canadian Experience Class | 18 | 57,750 | 507 | 523 |
| French language proficiency | 12 | 60,500 | 382 | 435 |
| Healthcare and social services occupations | 3 | 11,500 | 467 | 475 |
| Physicians with Canadian work experience | 3 | 891 | 169 | 223 |
| Senior managers with Canadian work experience | 3 | 1,000 | 389 | 429 |
| Trade occupations | 2 | 6,500 | 476 | 477 |
| Transport occupations | 2 | 450 | 470 | 477 |
| Skilled military recruits | 1 | 4 | 368 | 368 |

## Source and licence

All figures come from Immigration, Refugees and Citizenship Canada's official rounds of invitations data feed, https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json, which powers the Rounds of invitations page at https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations.html. Data retrieved October 30, 2026.

Contains information licensed under the Open Government Licence – Canada (https://open.canada.ca/en/open-government-licence-canada).

The compilation (cleaning, normalized categories, ISO dates and documentation) is released by crscalcu.ca under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). See the LICENSE file. crscalcu.ca is an independent site and is not affiliated with or endorsed by IRCC or the Government of Canada. Always confirm details on canada.ca before making immigration decisions.

## Processing notes

- Numbers were stripped of thousands separators; HTML was removed from text fields.
- Tie-breaking timestamps published in mixed formats (for example "August 31st, 2026 at 10:42:13 UTC") were converted to ISO 8601. For round #208, IRCC omitted the year ("October 7 at 16:38:21 UTC"), so the year of the round was used.
- No rows were added, removed or corrected. 2026 rows were cross-checked against crscalcu.ca's independently verified draw table with no differences.
- scripts/build.py rebuilds every file from the IRCC JSON.

## How to cite

crscalcu.ca (2026). Canada Express Entry Draws Dataset (CRS Cut-offs and Invitations). Data from Immigration, Refugees and Citizenship Canada, Open Government Licence – Canada. Updated October 30, 2026, through round #453. https://crscalcu.ca/latest-express-entry-draws-crs-cutoffs/

Please link to https://crscalcu.ca/ when you use or republish this data.
