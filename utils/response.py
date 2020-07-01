from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self,data_status=200, data_message=0, results=None, http_status=None, headers=None,
                 exception=False, **kwargs):
        data = {
            "status": data_status,
            "message": data_message
        }
        if results is not None:
            data['results'] = results
        data.update(kwargs)
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)
