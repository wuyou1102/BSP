"""Server URL Configuration

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
from django.conf.urls import include
from django.contrib import admin
import C2_DailyVersion
import C2_WeeklyVersion
import CommonRequest
import B2_DailyVersion
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', C2_DailyVersion.get_build_info),
                  url(r'^C2_DailyBuild/', C2_DailyVersion.get_build_info),
                  url(r'^C2_WeeklyBuild/', C2_WeeklyVersion.get_build_info),
                  url(r'^B2_DailyBuild/', include('Server.B2_DailyVersion.urls', namespace='B2_DailyBuild')),
                  url(r'^Download/', CommonRequest.download_file),
                  url(r'^Upload/', CommonRequest.upload_file),
                  url(r'^CommitHistory/', CommonRequest.commit_history),
                  url(r'^ReleaseNotes/', CommonRequest.release_notes),
                  url(r'^History/', CommonRequest.view_history),
                  url(r'^VersionConfig/', CommonRequest.version_number_config),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
