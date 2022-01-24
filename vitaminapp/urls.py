from django.contrib import admin
from django.urls import path     
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('products', views.products),
    path('product/<int:id>', views.one_product),
    path("main", views.loggedin),
    path('main/product/<int:id>', views.loggedin_product),
    path('login_register', views.login_register),
    path('admin/', admin.site.urls),  
    path('checkout', views.cart),
    path('register', views.register),
    path('login', views.login),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

