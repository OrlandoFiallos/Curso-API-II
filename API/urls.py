from django.urls import path 
from . import views
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path('categories',views.category_list),
    path('categories/<int:pk>',views.category_detail),
    path('menu-items/',views.menu_item_list),
    path('menu-items/<int:pk>',views.menu_item_detail),
    path('watches', views.WatchesViewSet.as_view({'get':'list'}),),
    path('watches/<int:pk>',views.WatchesViewSet.as_view({'get':'retrieve'})),
    path('secret',views.secret),
    path('api-token-auth',obtain_auth_token),#solo acepta POST
    path('manager-view', views.manager_view),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth)
]