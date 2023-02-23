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

q = "SecurityIncident"

q_ = list()

if from_ is not None:
    q_.append(f'TimeGenerated >= datetime("{from_}")')

if to_ is not None:
    q_.append(f'TimeGenerated >= datetime("{to_}")')

if q_:
    q += "\n| where " + " and ".join(q_)

q += """
| extend same = 1
| summarize count() by same"""


results = demisto.executeCommand(
    "azure-sentinel-query",
    {"query": q}
)

counts = []

for result in results:
    if not (
        isinstance(result, dict)
        and
        isinstance(lst := result.get("Contents"), list)
    ):
        continue
    for lst_ in lst:
        if (
            isinstance(lst_, dict)
            and
            isinstance(count_ := lst_.get("count_"), int)
        ):
            counts.append(count_)

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
