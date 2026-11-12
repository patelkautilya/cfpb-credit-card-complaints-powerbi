# Credit-card complaint operations | CFPB public data

**Status:** validated public dataset, saved two-page interactive Power BI report, and public PDF preview. The Power BI service link may require sign-in; the PDF and data in this repository are public.

## Business question

How did the volume, reported issue mix, and company-response categories change among **published credit-card complaints received in 2024 and 2025**?

## Source and reproduction

The source is the [Consumer Financial Protection Bureau's Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) and its [public search API](https://cfpb.github.io/ccdb5-api/). The [field reference](https://cfpb.github.io/api/ccdb/fields.html) defines complaint receipt date, product, issue, state, response category, timeliness, and complaint ID.

Run `python build_dataset.py` with Python 3.10+ from this folder. It requests the **Credit card** product for each of the 24 months in 2024–2025, downloads the official CSV export, and checks its row count against a separate JSON search total for that month. It checks product, date bounds, and globally unique complaint IDs. The script writes a row-level local extract, a smaller Power BI aggregate, and `validation_summary.json` with SHA-256 hashes. Monthly source exports are cached in `source_months/`; remove that local cache for a fresh snapshot. The published snapshot was downloaded on **2026-11-06** and will not silently change with the live database.

The Power BI source, `cfpb_credit_card_dashboard_2024_2025.csv`, has one row per **month × state × issue × company-response category × timely flag**, with `complaint_count` as its additive measure. Its **23,489 rows sum to 165,967 distinct complaint IDs**. The 36 MB row-level extract and monthly source cache are local reproduction outputs; the dashboard uses the 2 MB aggregate.

## Report and metric rules

- [Interactive Power BI report](https://app.powerbi.com/groups/e6426da3-9b36-4519-acf1-2434daa552ae/reports/f791f1ac-46a9-4e80-b004-5db304148266/0c4754ff44052a6b98c3?experience=power-bi) (Power BI sign-in may be required).
- [Two-page PDF export](CFPB_Credit_Card_Complaints_Report.pdf) and previews: [Overview](report-page-1.png), [Issue & State Detail](report-page-2.png). These are static snapshots of the report's default unfiltered state.
- **Overview:** complaint-count and timely-response KPIs, year range and state slicers, 24-month trend, issue ranking, and company-response mix. The count card abbreviates 165,967 as `166K`; exact totals are in the detail tables and findings.
- **Issue & State Detail:** sortable state and issue tables with exact counts and weighted timely-response shares, plus a monthly trend. Right-click an issue bar on Overview and choose **Drill through → Issue & State Detail** to inspect that issue; the blue back button returns to Overview.
- `Complaint count = SUM(complaint_count)`.
- `Timely response share = complaints with timely = Yes / all complaints in the active filter context`. Use weighted counts, never an average of grouped percentages.
- A state count is a **published complaint count**, not a complaint rate or a measure of market risk. The database lacks the number of customers or accounts needed for those rates.

## Interpretation limits

The CFPB says the database is **not a statistical sample** of consumer experiences. Complaints sent to companies are eligible for publication after a company response or 15 days, and the database generally updates daily. Company and state counts depend on company size, market share, population, awareness, and the complaint process. A timely company response is not proof that the consumer's problem was resolved. These descriptive comparisons do not establish causation or product safety.

See [validated findings](FINDINGS.md) and `validation_summary.json` for exact counts and caveats.


