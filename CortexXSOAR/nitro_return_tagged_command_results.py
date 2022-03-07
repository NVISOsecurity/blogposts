def nitro_return_tagged_command_results(command_result: CommandResults, tags: list):
    """
    Return tagged CommandResults

    :type command_result: ``CommandResults``
    :param command_result: CommandResults object to output with tags
    :type tags: ``list``
    :param tags: List of tags to add to war room entry

    """
    result = command_result.to_context()
    result['Tags'] = tags

    demisto.results(result)


results = [
    {
        'FileName': 'malware.exe',
        'FilePath': 'c:\\temp',
        'DetectionStatus': 'Detected'
    },
    {
        'FileName': 'evil.exe',
        'FilePath': 'c:\\temp',
        'DetectionStatus': 'Prevented'
    }
]
tags_to_add = ['evidence', 'malware']
title = "Malware Mitigation Status"

command_result = CommandResults(
        readable_output=tableToMarkdown(title, results, None, removeNull=True),
    )

nitro_return_tagged_command_results(command_result=command_result, tags=tags_to_add)
