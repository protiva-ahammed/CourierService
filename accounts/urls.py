from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from .import views

#
#from .views import   ProductListView , product_render_pdf_view ,render_pdf_view
#
#app_name='accounts'


urlpatterns = [
    
    path('',views.home,name='home'),
    path('about/',views.contract),
    path('account/',views.accountSettings,name='account'),
    path('user/',views.userPage,name='user-page'),
    path('products/',views.products,name='products'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),

    path('customers/<str:pk_test>/',views.customers, name='customer'),
    
    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
    
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),

    path('delete_orderG/<str:pk>/',views.deleteOrderG,name='delete_orderG'),
    path('update_orderG/<str:pk>/',views.updateOrderG,name='update_orderG'),

    path('generalorder/',views.generalorder,name='generalorder'),
    path('generalorderlist/',views.generalorderlist,name='generalorderlist'),
    path('generalorderlist/<str:pk>/',views.filledUp,name='filledUp'),
    # path('pdf/<str:pk>',views.pdf,name='pdf'),
    #path('pdf/<int:pk>',,name='generalorder_render_pdf_view'),

    

    
    #path('products/<str:pk>/',ProductListView.as_view(),name='product-pdf-view'),


    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
    

]
