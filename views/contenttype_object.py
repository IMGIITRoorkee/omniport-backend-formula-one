from rest_framework import generics, permissions, response, status
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType


class ContentTypeObjectList(generics.GenericAPIView):
    """
    This view serves the list of all objects inside a particular instance of
    the ContentType model
    """

    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ContentType.objects.all()

    def get(self, request, pk):
        """
        Returns the list of all objects in the format:
        {
            value *ID of the object*
            label *string representation of the object*
        }
        :param request: request object
        :param pk: ID of instance
        :return: list of objects
        """

        try:
            contenttype_object_type = ContentType.objects.get_for_id(pk)
        except ObjectDoesNotExist:
            return response.Response(
                ContentType.objects.none(),
                status=status.HTTP_404_NOT_FOUND,
            )

        contenttype_objects = (
            contenttype_object_type.model_class().objects.all()
        )
        contenttype_objects_choices = []

        for contenttype_object in contenttype_objects:
            contenttype_objects_choices.append(
                {
                    "value": contenttype_object.pk,
                    "label": str(contenttype_object),
                },
            )

        return response.Response(
            contenttype_objects_choices,
            status=status.HTTP_200_OK,
        )
