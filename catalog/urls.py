from django.urls import path
from . import views

urlpatterns = [
    path('replenish/<int:count>', views.replenish, name='replenish'),
    path('replenish/<int:count>', views.replenish, name='replenish'),
]
