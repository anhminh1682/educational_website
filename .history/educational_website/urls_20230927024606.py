from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]

handler404 = 'base.views.error'
handler500 = 'base.views.error'

#Thêm URLConf để phục vụ các tệp tĩnh từ thư mục staticfiles
urlpatterns = [

  url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

  url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

# Bổ sung URLConf cho các tệp phương tiện nếu cần
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)