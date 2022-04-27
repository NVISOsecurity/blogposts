import json


def nitro_execute_api_command(command: str, args: dict = None):
    """Execute a command using the Demisto REST API

    :type command: ``str``
    :param command: command to execute
    :type args: ``dict``
    :param args: arguments of command to execute

    :return: list of returned results of command
    :rtype: ``list``
    """
    args = args or {}

    # build the command string in the form !Command arg1="val1" arg2="val2"
    cmd_str = f"!{command}"

    for key, value in args.items():
        if isinstance(value, dict):
            value = json.dumps(json.dumps(value))
        else:
            value = json.dumps(value)
        cmd_str += f" {key}={value}"

    results = nitro_execute_command("demisto-api-post", {
        "uri": "/entry/execute/sync",
        "body": json.dumps({
            "investigationId": demisto.incident().get('id', ''),
            "data": cmd_str
        })
    })

    if not isinstance(results, list) \
            or len(results) == 0\
            or not isinstance(results[0], dict):
        return []

    results = results[0].get("Contents").get("response")
    for result in results:
        if "contents" in result:
            result["Contents"] = result.pop("contents")

    return results
