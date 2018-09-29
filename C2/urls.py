"""C2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import DailyVersion
import WeeklyVersion
import CommonRequest

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', DailyVersion.get_build_info),
                  url(r'^DailyBuild/', DailyVersion.get_build_info),
                  url(r'^WeeklyBuild/', WeeklyVersion.get_build_info),
                  url(r'^Download/', CommonRequest.download_file),
                  url(r'^Upload/', CommonRequest.upload_file),
                  url(r'^CommitHistory/', CommonRequest.commit_history),
                  url(r'^ReleaseNotes/', CommonRequest.release_notes),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
