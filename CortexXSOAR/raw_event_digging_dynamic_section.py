import json

def main():
    try:
        ret_notes = {}
        investigation_id = demisto.incident()["id"]
        uri = f"investigation/{investigation_id}"
        body = {
            "pageSize": 100,
            "categories": [],
            "tags": ["raw_data"],
            "notCategories": [],
            "usersAndOperator": False,
            "tagsAndOperator": False,
        }
        body = json.dumps(body, indent=4)
        args = {"uri": uri, "body": body}
        res_cmd = demisto.executeCommand("demisto-api-post", args)
        for res in res_cmd:
            if not (isinstance(res, dict) and isinstance(contents := res.get("Contents"), dict)):
                continue
            if not isinstance(response := contents.get("response"), dict):
                continue
            if not isinstance(entries := response.get("entries"), (list, List)):
                continue
            for entry in entries:
                key = ""
                if not isinstance(entry, dict):
                    continue
                if isinstance(entry_id := entry.get("id"), str):
                    key += entry_id
                if isinstance(entry_task := entry.get("entryTask"), dict):
                    if isinstance(task_name := entry_task.get("taskName"), str):
                        key += " - " + task_name
                value = None
                if isinstance(cnt := entry.get("contents"), str):
                    try:
                        value = json.loads(cnt)
                    except Exception:
                        value = cnt
                ret_notes.update({key: value})

        ret_labels = {}
        incident = demisto.incident()
        if not (isinstance(incident, dict) and "labels" in incident.keys()):
            continue
        labels = incident["labels"]
        if not isinstance(labels, (list, List)):
            continue
        for label in labels:
            if not isinstance(label, dict):
                continue
            label_type, label_value = label.get("type"), label.get("value")
            if not (isinstance(label_type, str) and isinstance(label_value, str)):
                continue
            try:
                label_value = json.loads(label_value)
            except Exception:
                pass
            try:
                ret_labels.update({label_type: label_value})
            except Exception:
                pass
        ret = {
            "notes": ret_notes,
            "labels": ret_labels
        }
        results = CommandResults(raw_response=ret)
        return_results(results)
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f"Failed to execute BaseScript. Error: {str(ex)}")


""" ENTRY POINT """

if __name__ in ("__main__", "__builtin__", "builtins"):
    main()
