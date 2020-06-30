from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.response import Response
def exception_handler(exc,context):
    error = "%s %s %s" % (context['view'],context['request'].method,exc)
    print(error)
    response = drf_exception_handler(exc,context)
    if response is None:
        return Response(
            {"error":"程序走神了，请稍等"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            exception=None
        )
    return response