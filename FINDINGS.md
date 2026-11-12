# Findings and limits | CFPB credit-card complaints

**Snapshot:** CFPB public complaints with product `Credit card` and date received from 2024-01-01 through 2025-12-31, downloaded 2026-11-06. These are published complaint records, not all consumer experiences or all complaints submitted to the CFPB.

## Validation

- 165,967 unique complaint IDs; the 24 monthly CSV exports each reconcile exactly to an independent API search total.
- 75,989 records were received in 2024 and 89,978 in 2025. The latter is **18.41% more published records** in this fixed extract. This is a count change, not a change in the probability that a consumer has a problem.
- The Power BI aggregate has 23,489 rows; its `complaint_count` sums exactly to 165,967.
- `Timely response?` is `Yes` for 165,484 records and `No` for 483, an observed **99.71%** timely-response share. The shares are 99.82% in 2024 and 99.62% in 2025. The metric reports the CFPB field; it does not measure consumer satisfaction or resolution.

## Patterns to explore

- `Problem with a purchase shown on your statement` is the most frequent issue in both years: 14,595 records (19.21% of 2024 credit-card complaints) and 19,810 (22.02% of 2025), a 2.81 percentage-point increase in the **issue mix**. Product and issue labels are those published in the database.
- January 2025 has the highest monthly count in this panel, 9,073. The dashboard should expose all 24 monthly values and allow a user to inspect whether a pattern is sustained.
- The most common company-response category across the two years is `Closed with explanation` (106,337 records). This is an administrative response category, not an independently verified outcome.

## What the data cannot answer

The [CFPB](https://www.consumerfinance.gov/data-research/consumer-complaints/) warns that its database is not representative of all consumer experiences. It excludes some complaints referred to other regulators, and publication timing and later updates can change a historical extract. Counts by state or company lack population, customer, account, and transaction denominators. Response timeliness and closure labels do not prove the quality of resolution. We therefore avoid claims about company performance, consumer risk, or the causes of the observed changes.
