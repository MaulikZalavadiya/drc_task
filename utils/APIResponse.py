from rest_framework.response import Response
from http.client import responses as HTTPStatus



def APIResponse(data=None, notification=None, *args, **kwargs):
    response = {
        'notification': {}
    }
    if (notification is not None) and len(notification) == 2:
        response['notification'] = {
            'type': notification[0],
            'message': notification[1]
        }
    if data is None:
        response['data'] = []
    else:
        response['data'] = data
    resp = Response(response, *args, **kwargs)
    resp.data['status'] = resp.status_code
    resp.data['status_type'] = HTTPStatus[resp.status_code]
    return resp