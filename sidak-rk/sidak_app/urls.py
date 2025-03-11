from django.urls import path
from . import views

urlpatterns = [
    # login
    path('', views.login, name='login'), 
    # Lupa Kata Sandi/Forgot Password
    path('forgot-password/', views.forgotpassword, name='forgotpassword'), 
    path('verify/', views.verify, name='verify'), 
    path('reset-password/', views.resetpassword, name='resetpassword'), 
    path('new-password/', views.setnew, name='setnew'), 

    # admin
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'), 
    path('data-ajuan/', views.data_ajuan, name='data_ajuan'), 
    path('history/', views.history, name='history'),

    # karyawan
    path('dashboard/', views.dashboard_karyawan, name='dashboard_karyawan'),
]
