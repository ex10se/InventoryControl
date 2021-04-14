from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from warehouse.views import TotalCostView, ItemView, index

urlpatterns = [
    path('', index),
    url(r'^resources/$', ItemView.as_view()),
    path('total_cost', TotalCostView.as_view()),
    path('admin/', admin.site.urls),
]
