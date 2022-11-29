res = demisto.executeCommand("azure-sentinel-query", {
    "query": """SecurityIncident
| where TimeGenerated between (datetime("2022-10-01T00:00:00+00:00")..datetime("2022-11-01T00:00:00+00:00"))
| extend same = 1
| union (
SecurityIncident
| where TimeGenerated between (datetime("2022-09-01T00:00:00+00:00")..datetime("2022-10-01T00:00:00+00:00"))
| extend same = 2)
| summarize count() by same"""
})

this_month_counts = list()
last_month_counts = list()

lookup = {
    1: this_month_counts,
    2: last_month_counts
}

for res_ in res:
    if isinstance(res_, dict) and isinstance(lst := res_.get("Contents"), list):
        for lst_ in lst:
            if isinstance(lst_, dict):
                if isinstance(tgt_ := lst_.get("same"), int):
                    tgt = lookup.get(tgt_)
                    if tgt is not None and isinstance(count_ := lst_.get("count_"), int):
                        tgt.append(count_)

total_this_month_counts = sum(this_month_counts)
total_last_month_counts = sum(last_month_counts)

demisto.results(
    {
        "Type": 17,
        "ContentsFormat": "number",
        "Contents": {
             "stats": { "prevSum": total_last_month_counts, "currSum": total_this_month_counts},
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
)