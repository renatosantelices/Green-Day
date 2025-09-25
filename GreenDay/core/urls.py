from django.urls import path
from . import views


urlpatterns = [
    path('', views.catalogo, name='home'),   # raíz muestra catálogo
    path('catalogo/', views.catalogo, name='catalogo'),  # opcional, si quieres mantener /catalogo
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedidos/', views.historial_pedidos, name='historial_pedidos'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

]

