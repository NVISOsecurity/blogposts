import json


def nitro_execute_http_request(method: str, uri: str, body: dict = None) -> dict:
    """
    Send internal http requests to XSOAR server

    :type method: ``str``
    :param method: HTTP Method (GET / POST / PUT / DELETE)
    :type uri: ``str``
    :param uri: Request URI
    :type body: ``dict``
    :param body: Body of request

    :return: dict of response body
    :rtype: ``dict``
    """

    response = demisto.internalHttpRequest(method, uri, body)
    response_body = json.loads(response.get('body'))

    if response.get('statusCode') != 200:
        raise Exception(f"Func: nitro_execute_http_request; {response.get('status')}: {response_body.get('detail')}; "
                        f"error: {response_body.get('error')}")
    else:
        return response_body
