FromDate, ToDate = NitroDateFactory.from_regular_xsoar_date_range_args(demisto.args())

is_dashboard = demisto.args().get("widgetType") is not None

from_ = "2022-10-01T00:00:00+00:00"
to_ = "2022-11-01T00:00:00+00:00"

if is_dashboard:
    if isinstance(FromDate, NitroRegularDate):
        from_ = FromDate.to_iso8601()
    else:
        from_ = None
    if isinstance(ToDate, NitroRegularDate):
        to_ = ToDate.to_iso8601()
    else:
        to_ = None

query = "SecurityIncident"

tmp_query_list = list()

if from_ is not None:
    tmp_query_list.append(f'TimeGenerated >= datetime("{from_}")')

if to_ is not None:
    tmp_query_list.append(f'TimeGenerated >= datetime("{to_}")')

if tmp_query_list:
    query += "\n| where " + " and ".join(tmp_query_list)

query += """
| extend same = 1
| summarize count() by same"""


results = demisto.executeCommand(
    "azure-sentinel-query",
    {"query": query}
)

counts = []

for result in results:
    if not (
        isinstance(result, dict)
        and
        isinstance(contents := result.get("Contents"), list)
    ):
        continue
    for content in contents:
        if (
            isinstance(content, dict)
            and
            isinstance(count := content.get("count_"), int)
        ):
            counts.append(count)

total_count = sum(counts)

data = {
    "Type": 17,
    "ContentsFormat": "number",
    "Contents": {
        "stats": total_count,
        "params": {
            "name": "Incidents Last Month",
            "colors": {"items": {
                "green": {"value": 40}
            }},
        },
    },
}


if is_dashboard:
    demisto.results(total_count)
else:
    demisto.results(data)
