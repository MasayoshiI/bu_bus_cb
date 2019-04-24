from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import BUsBot.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", BUsBot.views.index, name="index"),
    path("df/", BUsBot.views.df, name="df"),
    path("privacypolicy/", BUsBot.views.privacypolicy, name="privacypolicy"),
    path("alert/", BUsBot.views.alert, name="alert"),
    path("admin/", admin.site.urls),
    
]
