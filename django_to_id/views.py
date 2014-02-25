from models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from serializers import serialize_node
from rest_framework import status


class NodeViewSet(APIView):
    """
    Retrieve, update or delete a single i9 instance.
    """

    def get(self, request, id, format=None):
        try:
            model_node = Node.objects.get(id=id)
        except:
            return Response("node not found", status=status.status.HTTP_404_NOT_FOUND)

        data = serialize_node(model_node)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)
