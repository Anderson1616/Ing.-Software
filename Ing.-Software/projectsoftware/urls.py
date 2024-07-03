from django.contrib import admin
from django.urls import path
from prueba import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/Home', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # Nueva URL para login
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('agregar_pedido/', views.agregar_pedido_view, name='agregar_pedido'),
    path('ver_informacion/<int:pedido_id>/', views.ver_informacion, name='ver_informacion'),
    path('editar_pedido/<int:pedido_id>/', views.editar_pedido, name='editar_pedido'),
    path('eliminar_pedido/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),

    path('crud_pedidos/', views.crud_pedidos, name='crud_pedidos'),

    path('agregar_conductor/', views.agregar_conductor, name='agregar_conductor'),
    path('crud_conductores/', views.crud_conductores, name='crud_conductores'),
    path('eliminar_conductor/<int:conductor_id>/', views.eliminar_conductor, name='eliminar_conductor'),
    path('editar_conductor/<int:conductor_id>/', views.editar_conductor, name='editar_conductor'),
    path('ver_info_conductor/<int:conductor_id>/', views.ver_info_conductor, name='ver_info_conductor'),
    
    path('agregar_camion/', views.agregar_camion, name='agregar_camion'),
    path('crud_camion/', views.crud_camion, name='crud_camion'),
    path('eliminar_camion/<int:camion_id>/', views.eliminar_camion, name='eliminar_camion'),
    path('editar_camion/<int:camion_id>/', views.editar_camion, name='editar_camion'),
    path('ver_info_camion/<int:camion_id>/', views.ver_info_camion, name='ver_info_camion'),

    path('crud_pedidos/', views.crud_pedidos, name='crud_pedidos'),
     path('buscar_pedidos/', views.buscar_pedidos, name='buscar_pedidos')
]
