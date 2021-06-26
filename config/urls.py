from django.contrib import admin
from django.urls import path, include
from notify import views   #追加
import notifications.urls 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('', views.MessageSendView.as_view(), name='index'),
    path('^delete/(?P<slug>\d+)/$', views.delete, name='delete'),
]
