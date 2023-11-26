from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomUserDeleteView(APIView):
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
