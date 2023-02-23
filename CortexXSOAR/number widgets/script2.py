FromDate, ToDate = NitroDateFactory.from_regular_xsoar_date_range_args(demisto.args())

is_dashboard = demisto.args().get("widgetType") is not None

from_ = "2022-10-01T00:00:00+00:00"
to_ = "2022-11-01T00:00:00+00:00"

from_2 = "2022-09-01T00:00:00+00:00"
to_2 = "2022-10-01T00:00:00+00:00"

if is_dashboard:
    if isinstance(FromDate, NitroRegularDate):
        if isinstance(ToDate, NitroRegularDate):
            td = ToDate.date
        else:
            td = datetime.now(timezone.utc)
        delta = td - FromDate.date
        from2 = NitroRegularDate(date=FromDate.date - delta)
        to2 = FromDate
    else:
        from2 = FromDate
        to2 = ToDate

    if isinstance(FromDate, NitroRegularDate):
        from_ = FromDate.to_iso8601()
    else:
        from_ = None
    if isinstance(ToDate, NitroRegularDate):
        to_ = ToDate.to_iso8601()
    else:
        to_ = None
    if isinstance(from2, NitroRegularDate):
        from_2 = from2.to_iso8601()
    else:
        from_2 = None
    if isinstance(to2, NitroRegularDate):
        to_2 = to2.to_iso8601()
    else:
        to_2 = None

query = "SecurityIncident"

tmp_query_list = list()

if from_ is not None:
    tmp_query_list.append(f"TimeGenerated >= datetime(\"{from_}\")")

if to_ is not None:
    tmp_query_list.append(f"TimeGenerated < datetime(\"{to_}\")")

if tmp_query_list:
    query += "\n| where " + " and ".join(tmp_query_list)

query += """
| extend same = 1
| union (
SecurityIncident"""

tmp_query_list2 = list()

if from_2 is not None:
    tmp_query_list2.append(f"TimeGenerated >= datetime(\"{from_2}\")")

if to_2 is not None:
    tmp_query_list2.append(f"TimeGenerated < datetime(\"{to_2}\")")

if tmp_query_list2:
    query += "\n| where " + " and ".join(tmp_query_list2)

query += """
| extend same = 2)
| summarize count() by same"""

results = demisto.executeCommand("azure-sentinel-query", {
    "query": query
})

this_month_counts = list()
last_month_counts = list()

lookup = {
    1: this_month_counts,
    2: last_month_counts
}

for result in results:
    if not (
        isinstance(result, dict)
        and
        isinstance(contents := result.get("Contents"), list)
    ):
        continue
    for content in contents:
        if not isinstance(content, dict):
            continue
        if not isinstance(raw_same_target := content.get("same"), int):
            continue
        same_target = lookup.get(raw_same_target)
        if (
            same_target is not None
            and
            isinstance(count := content.get("count_"), int)
        ):
            same_target.append(count)

total_this_month_counts = sum(this_month_counts)
total_last_month_counts = sum(last_month_counts)

stats = {
    "prevSum": total_last_month_counts,
    "currSum": total_this_month_counts
}

data = {
    "Type": 17,
    "ContentsFormat": "number",
    "Contents": {
        "stats": stats,
        "params": {
            "name": "Incidents Last Month",
            "colors": {
                "items": {
                    "green": {
                        "value": 40
                    }
                }
            }
        }
    }
}



if is_dashboard:
    demisto.results(stats)
else:
    demisto.results(data)