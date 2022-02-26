def nitro_execute_command(command: str, args: dict = None, retry: int = 3, fail_on_error=True) -> list:
    """Wrapper function with error handling an retry logic for demisto.executeCommand()

    :type command: ``str``
    :param command: command to execute
    :type args: ``dict``
    :param args: arguments of command to execute
    :type retry: ``int``
    :param retry: retry count if error occurred
    :type fail_on_error: ``Bool``
    :param fail_on_error: Fail the command when receiving an error from the command

    :return: list of returned results of demisto.executeCommand()
    :rtype: ``list``
    """

    args = args or {}
    error_result = {}
    _exception = None

    for i in range(0, retry, 1):
        error = False
        exception = False

        try:
            results = demisto.executeCommand(command, args)
        except Exception as ex:
            _exception = ex
            results = []
            exception = True

        if results:
            for result in results:
                if not isinstance(result, dict) or result.get("Type") == 4:
                    error = True
                    error_result = result
        else:
            error = True
            error_result = {}

        if not error and not exception:
            break

    if exception:
        if fail_on_error:
            raise _exception
    elif error:
        if fail_on_error:
            raise Exception(
                f"Error when executing command: {command} with arguments: {args}: {error_result.get('Contents')}")

    return results
