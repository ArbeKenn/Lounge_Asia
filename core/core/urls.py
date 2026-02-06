from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('shop.urls')),
    # path('api/orders/', include('orders.urls')),
    path('api/users/', include('users.urls')),
    # path('api/pay/', include('pay.urls')),
]
