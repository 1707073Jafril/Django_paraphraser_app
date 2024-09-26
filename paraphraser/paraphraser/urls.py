# paraphraser/urls.py

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paraphrase/', include('paraphrase.urls')),  # Include your paraphrase app URLs
    path('', RedirectView.as_view(url='/paraphrase/', permanent=True)),  # Redirect root to paraphrase
]
