from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('list/', views.list, name="list"),
    path('create/', views.create_view, name="create"),
    path('<int:id>/update', views.update_view, name="update"),
    path('<int:id>/delete', views.delete_view, name="delete"),
    path('<int:id>', views.detail, name="detail"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]

