from django.urls import path

from formula_one.views.contenttype_object import ContentTypeObjectList
from formula_one.views.csrf import EnsureCsrf
from formula_one.views.hello import Hello
from formula_one.views.manifest import Manifest

app_name = 'formula_one'

urlpatterns = [
    path('hello/', Hello.as_view(), name='hello'),
    path('ensure_csrf/', EnsureCsrf.as_view(), name='ensure_csrf'),
    path('manifest/', Manifest.as_view(), name='manifest'),
    path(
        'contenttype_object/<int:pk>/',
        ContentTypeObjectList.as_view(),
        name='contenttype_objects',
    ),
]
