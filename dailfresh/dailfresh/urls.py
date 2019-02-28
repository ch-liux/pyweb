
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls', namespace='users')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('goods/', include('apps.goods.urls', namespace='goods')),
    re_path('^tinymce/', include('tinymce.urls')),    #富文本编辑器
]
