number = 53

data = {
    "Type": 17,
    "ContentsFormat": "number",
    "Contents": {
        "stats": number,
        "params": {
            "layout": "horizontal",
            "name": "Lala",
            "sign": "@",
            "colors": {
                "items": {
                    "#00CD33": {
                        "value": 10
                    },
                    "#FAC100": {
                        "value": 20
                    },
                    "green": {
                        "value": 40
                    },
                }
            },
            "type": "above",
        },
    },
}

is_dashboard = demisto.args().get("widgetType") is not None

if is_dashboard:
    demisto.results(number)
else:
    demisto.results(data)
