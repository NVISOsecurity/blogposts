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

q = "SecurityIncident"

q_ = list()

if from_ is not None:
    q_.append(f"TimeGenerated >= datetime(\"{from_}\")")

if to_ is not None:
    q_.append(f"TimeGenerated < datetime(\"{to_}\")")

if q_:
    q += "\n| where " + " and ".join(q_)

q += """
| extend same = 1
| union (
SecurityIncident"""

q__ = list()

if from_2 is not None:
    q__.append(f"TimeGenerated >= datetime(\"{from_2}\")")

if to_2 is not None:
    q__.append(f"TimeGenerated < datetime(\"{to_2}\")")

if q__:
    q += "\n| where " + " and ".join(q__)

q += """
| extend same = 2)
| summarize count() by same"""

res = demisto.executeCommand("azure-sentinel-query", {
    "query": q
})

this_month_counts = list()
last_month_counts = list()

lookup = {
    1: this_month_counts,
    2: last_month_counts
}

for res_ in res:
    if not (
        isinstance(res_, dict)
        and
        isinstance(lst := res_.get("Contents"), list)
    ):
        continue
    for lst_ in lst:
        if not isinstance(lst_, dict):
            continue
        if not isinstance(tgt_ := lst_.get("same"), int):
            continue
        tgt = lookup.get(tgt_)
        if tgt is not None and isinstance(count_ := lst_.get("count_"), int):
            tgt.append(count_)

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