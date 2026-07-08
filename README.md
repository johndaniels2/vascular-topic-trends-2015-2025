# Topic Trends in Vascular Surgery Conference Presentations (2015–2025)

Code and data for a study comparing vascular surgery meeting content with
trainee examination and operative benchmarks (manuscript in preparation).

## Overview
Podium presentation titles from six North American vascular surgery societies
(2015–2025) were classified into disease-based topics using a MeSH-derived
keyword model, then compared with the VSITE examination blueprint and ACGME
operative case-log data across seven clinical domains.

## Repository contents
- `svstitles.csv`, `savstitles.csv`, `csvstitles.csv`,
  `wvstitles.csv`, `nesvstitles.csv`, `scvstitles.csv`
  — podium presentation titles, one file per society
- `Chi_Square_Goodness_of_Fit.ipynb` — goodness-of-fit test of conference
  distribution vs. the VSITE and ACGME benchmarks

## Societies
Society for Vascular Surgery (SVS), Southern Association for Vascular Surgery
(SAVS), Canadian Society for Vascular Surgery (CSVS), Western Vascular Society
(WVS), New England Society for Vascular Surgery (NESVS), and Society for
Clinical Vascular Surgery (SCVS).

## Data sources
- Conference titles: publicly available society meeting programs
- VSITE content blueprint (American Board of Surgery)
- ACGME 2024–2025 National Resident Report case logs

## Requirements
Python 3, pandas, scipy

## Reference
Accompanies the manuscript *Vascular Surgery Meeting Content Emphasizes
Examination Priorities Over Operative Training Experience* (in preparation).
