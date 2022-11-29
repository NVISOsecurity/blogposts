res = demisto.executeCommand("azure-sentinel-query", {
    "query": """SecurityIncident
| where TimeGenerated between (datetime("2022-10-01T00:00:00+00:00")..datetime("2022-11-01T00:00:00+00:00"))
| extend same = 1
| summarize count() by same"""
})

counts = []

for res_ in res:
    if isinstance(res_, dict) and isinstance(lst := res_.get("Contents"), list):
        for lst_ in lst:
            if isinstance(lst_, dict) and isinstance(count_ := lst_.get("count_"), int):
                counts.append(count_)

total_count = sum(counts)

demisto.results(
    {
        "Type": 17,
        "ContentsFormat": "number",
        "Contents": {
            "stats": total_count,
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