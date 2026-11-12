"""Reproduce a fixed 2024-2025 CFPB credit-card complaint extract.

Downloads one calendar month per official CFPB CSV export to stay within the
API's export limit. Independently checks each month's JSON search total.
"""

import csv
import hashlib
import io
import json
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/'
OUT = Path(__file__).resolve().parent
FIELDS = ['complaint_id', 'date_received', 'year', 'month', 'product', 'sub_product',
          'issue', 'sub_issue', 'state', 'submitted_via', 'company_response', 'timely']
MAPPING = {
    'Complaint ID': 'complaint_id', 'Date received': 'date_received',
    'Product': 'product', 'Sub-product': 'sub_product', 'Issue': 'issue',
    'Sub-issue': 'sub_issue', 'State': 'state', 'Submitted via': 'submitted_via',
    'Company response to consumer': 'company_response', 'Timely response?': 'timely',
}


def fetch(params):
    url = BASE + '?' + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=90) as response:
                return response.read()
        except HTTPError as error:
            if error.code != 429 or attempt == 5:
                raise
            wait = int(error.headers.get('Retry-After', '0') or '0')
            wait = min(120, max(wait, 10 * (attempt + 1)))
            print(f'CFPB rate limit; waiting {wait}s before retry', flush=True)
            time.sleep(wait)


def months():
    for year in (2024, 2025):
        for month in range(1, 13):
            start = date(year, month, 1)
            end = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
            yield start, end


def main():
    seen = set()
    rows = []
    checks = []
    cache = OUT / 'source_months'
    cache.mkdir(exist_ok=True)
    for start, end in months():
        params = {'date_received_min': start.isoformat(), 'date_received_max': end.isoformat(),
                  'product': 'Credit card', 'no_aggs': 'true'}
        stamp = start.strftime('%Y-%m')
        csv_cache = cache / f'{stamp}.csv'
        count_cache = cache / f'{stamp}.count.json'
        if csv_cache.exists():
            raw = csv_cache.read_bytes()
        else:
            raw = fetch({**params, 'format': 'csv'})
            csv_cache.write_bytes(raw)
        reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
        missing = set(MAPPING) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'{start}: missing columns {sorted(missing)}')
        count = 0
        for source in reader:
            row = {target: (source[name] or '').strip() for name, target in MAPPING.items()}
            if row['product'] != 'Credit card':
                raise ValueError(f'{start}: unexpected product {row["product"]!r}')
            day = datetime.fromisoformat(row['date_received'].replace('Z', '+00:00')).date()
            if not start <= day <= end:
                raise ValueError(f'{start}: out-of-month date {day}')
            if not row['complaint_id'] or row['complaint_id'] in seen:
                raise ValueError(f'{start}: missing/duplicate complaint ID {row["complaint_id"]}')
            seen.add(row['complaint_id'])
            row['year'] = str(start.year)
            row['month'] = start.strftime('%Y-%m')
            rows.append(row)
            count += 1
        if count_cache.exists():
            total = json.loads(count_cache.read_text(encoding='utf-8'))['total']
        else:
            total = json.loads(fetch({**params, 'size': 1}))['hits']['total']['value']
            count_cache.write_text(json.dumps({'total': total}), encoding='utf-8')
        if count != total:
            raise ValueError(f'{start}: CSV {count} differs from search total {total}')
        checks.append({'month': start.strftime('%Y-%m'), 'records': count,
                       'source_csv_sha256': hashlib.sha256(raw).hexdigest()})
        print(f'{start:%Y-%m}: {count:,} complaints, count reconciled', flush=True)
        if not (csv_cache.exists() and count_cache.exists()):
            time.sleep(1)

    path = OUT / 'cfpb_credit_card_complaints_2024_2025.csv'
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    grouped = Counter((r['month'], r['year'], r['state'], r['issue'],
                       r['company_response'], r['timely']) for r in rows)
    aggregate_path = OUT / 'cfpb_credit_card_dashboard_2024_2025.csv'
    with aggregate_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['month', 'year', 'state', 'issue', 'company_response',
                         'timely', 'complaint_count'])
        for key, count in sorted(grouped.items()):
            writer.writerow([*key, count])
    if sum(grouped.values()) != len(rows):
        raise ValueError('Aggregate complaint count does not reconcile to row-level data')
    summary = {
        'source': BASE, 'product': 'Credit card', 'received_period': ['2024-01-01', '2025-12-31'],
        'record_count': len(rows), 'unique_complaint_ids': len(seen),
        'year_counts': dict(sorted(Counter(r['year'] for r in rows).items())),
        'timely_counts': dict(Counter(r['timely'] or '(missing)' for r in rows)),
        'top_issues': Counter(r['issue'] or '(missing)' for r in rows).most_common(12),
        'monthly_checks': checks,
        'curated_csv_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'dashboard_rows': len(grouped),
        'dashboard_count_sum': sum(grouped.values()),
        'dashboard_csv_sha256': hashlib.sha256(aggregate_path.read_bytes()).hexdigest(),
    }
    (OUT / 'validation_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(f'Validated {len(rows):,} unique complaints; wrote {path.name} and '
          f'{aggregate_path.name} ({len(grouped):,} aggregate rows)', flush=True)


if __name__ == '__main__':
    main()
