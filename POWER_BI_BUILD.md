# Power BI build specification

Use `cfpb_credit_card_dashboard_2024_2025.csv` as the source and name its table `Complaints`. The file is a fixed 2026-11-06 snapshot of published CFPB credit-card complaints received in 2024–2025. Set `year` and `complaint_count` to whole number; keep `month` as `YYYY-MM` text so it sorts chronologically; treat state, issue, company_response, and timely as text. Use Import mode if the service permits it.

## Measures

```DAX
Complaint Count = SUM('Complaints'[complaint_count])

Timely Complaints =
CALCULATE(
    [Complaint Count],
    'Complaints'[timely] = "Yes"
)

Timely Response Share =
DIVIDE([Timely Complaints], [Complaint Count])
```

Format `Timely Response Share` as a percentage with two decimal places. This ratio is weighted by complaint counts under the active filter context; do not average grouped percentages.

## Page 1 — Complaint overview

- Header: “Credit-card complaints | 2024–2025” with source and snapshot caption.
- Slicers: `year` (single or multi-select), `state` (searchable), and `issue` (searchable). Provide a clear-filters control if supported.
- KPI cards: `Complaint Count`, `Timely Complaints`, `Timely Response Share`.
- Column chart: `month` on x-axis, `Complaint Count` on y-axis. Display all 24 months, sorted ascending.
- Horizontal bar chart: top ten `issue` values by `Complaint Count`, descending; tooltip includes full issue name and count. The top-ten filter is visual-only; it must not change the KPI denominator.
- Footer: “Published complaint counts; no consumer or account denominator. A timely response does not establish resolution.”

## Page 2 — Issue and response review

- Reuse year, state, and issue slicers or sync them across pages where supported.
- Stacked bar or column chart: `company_response` by `Complaint Count`, segmented by `year`.
- Matrix/table: `state`, `issue`, `company_response`, `Complaint Count`, and `Timely Response Share`; enable sorting by count. Restrict initial display to a manageable number of rows if necessary, without changing the KPI totals.
- Add drill-through on `issue` if the editor supports it; show a selected issue's monthly trend and response mix on the detail page. If not supported, use cross-filter selection on the issue bar chart and describe that interaction accurately.
- Use a restrained dark navy background, contrasting teal and amber accents, and consistent count/percent units. Check labels and contrast at typical laptop size.

## Acceptance checks

- With no slicer selections: 165,967 complaints, 165,484 timely, 99.71% timely share.
- 2024 selected: 75,989 complaints; 2025 selected: 89,978 complaints. The month chart should show 12 months per selected year.
- January 2025: 9,073 complaints. The most frequent issue overall is “Problem with a purchase shown on your statement” with 34,405 complaints.
- Selecting a state or issue changes the cards and trend consistently; clearing filters restores the full totals.
- Export both pages to PDF and check that no visuals, titles, or caveats are clipped. The static export is a snapshot; the saved Power BI report is the interactive artifact.

These values come from `validation_summary.json` and `FINDINGS.md`. Do not substitute the CFPB site-wide 99% timely statistic for this filtered extract's measure.
