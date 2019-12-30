from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic.base import TemplateView


class ContentTypeObjectList(LoginRequiredMixin, TemplateView):
    """
    This view shows the list of all objects inside a particular instance of a
    ContentType model
    """

    template_name = 'formula_one/contenttype_object_list.html'
    paginate_by = 10

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
            raise Http404('ContentType does not exist')

        contenttype_objects = (
            contenttype_object_type.model_class().objects.all()
        )
        contenttype_objects_choices = []

        for contenttype_object in contenttype_objects:
            contenttype_objects_choices.append(
                {
                    'id': contenttype_object.pk,
                    'label': str(contenttype_object),
                },
            )

        paginator = Paginator(contenttype_objects_choices, self.paginate_by)
        page = self.request.GET.get('page')
        contenttype_object_list = paginator.get_page(page)

        context = {
            'contenttype_object_list': contenttype_object_list,
            'model': contenttype_object_type.model,
        }

        return context
