def return_tagged_results(title: str, results: [dict, list], tags: list):
    """
    Output as war room entry and add tags

    :type title: ``str``
    :param title: title of war room entry
    :type results: ``dict, list``
    :param results: dict or list to output as war room entry
    :type tags: ``list``
    :param tags: List of tags to add to war room entry

    """

    command_result = CommandResults(
        readable_output=tableToMarkdown(title, results, None, removeNull=True),
    ).to_context()

    command_result['Tags'] = tags

    demisto.results(command_result)


entry_results = [
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

return_tagged_results(title=entry_title, results=entry_results, tags=tags_to_add)
