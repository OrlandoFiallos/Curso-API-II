from django.urls import path 
from . import views
urlpatterns = [
    path('categories/',views.category_list),
    path('categories/<int:pk>',views.category_detail),
    path('menu-items/',views.menu_item_list),
    path('menu-items/<int:pk>',views.menu_item_detail)
]