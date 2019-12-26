from django.urls import path

from formula_one.views.csrf import EnsureCsrf
from formula_one.views.hello import Hello
from formula_one.views.manifest import Manifest

app_name = 'formula_one'

urlpatterns = [
    path('hello/', Hello.as_view(), name='hello'),
    path('ensure_csrf/', EnsureCsrf.as_view(), name='ensure_csrf'),
    path('manifest/', Manifest.as_view(), name='manifest'),
]
