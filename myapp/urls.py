from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    path(r'products/', views.products, name='products'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'order_response/', views.place_order, name='order_response'),
    path(r'products/<int:prod_id>/', views.productdetail, name='productdetail'),
    path(r'interest_confirmation/', views.productdetail, name='interestresponse'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'orders/', views.myorders, name='orders'),
    path(r'register/', views.user_register, name='register'),
    path(r'password_reset/', views.forgot_password, name='password_reset'),
    path(r'password_reset/<int:done>', views.password_reset_done, name="password_reset_complete")

]
