def return_tagged_results(title: str, result: [dict, list], tags: list):
    """
    Output as war room entry and add tags

    :type title: ``str``
    :param title: title of war room entry
    :type result: ``dict, list``
    :param result: dict or list to output as war room entry
    :type tags: ``list``
    :param tags: List of tags to add to war room entry

    """

    command_result = CommandResults(
        readable_output=tableToMarkdown(title, result, None, removeNull=True),
    ).to_context()

    command_result['Tags'] = tags

    demisto.results(command_result)


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
entry_title = "Malware Mitigation Status"

return_tagged_results(title=entry_title, result=results, tags=tags_to_add)
