from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.contenttypes.models import ContentType


class ContentTypeObjectList(LoginRequiredMixin, TemplateView):
    """
    This view shows the list of all objects inside a particular instance of a
    ContentType model
    """

    template_name = 'formula_one/contenttype_object_list.html'

    def get_context_data(self, **kwargs):
        """
        Return the list of all objects inside the ContentType model class and 
        the name of the ContentType model
        :return: context for template
        """

        pk = self.kwargs['pk']

        try:
            contenttype_object_type = ContentType.objects.get_for_id(pk)
        except ObjectDoesNotExist:
            raise Http404("ContentType does not exist")

        contenttype_objects = (
            contenttype_object_type.model_class().objects.all()
        )
        contenttype_objects_choices = []

        for contenttype_object in contenttype_objects:
            contenttype_objects_choices.append(
                {
                    "id": contenttype_object.pk,
                    "label": str(contenttype_object),
                },
            )

        context = {
            "contenttype_objects_list": contenttype_objects_choices,
            "model": contenttype_object_type.model,
        }

        return context
