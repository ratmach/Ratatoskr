
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import patterns as patterns
from django.contrib.staticfiles import views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),

]

urlpatterns += [
    url(r'^static/js/DataClass.js', views.serve),
]

urlpatterns += staticfiles_urlpatterns()
