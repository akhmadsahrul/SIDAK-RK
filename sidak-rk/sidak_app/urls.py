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

    # Ubah Kata sandi profile
    path('ubah-sandi/', views.ubah_katasandi, name='ubah_katasandi'),

    # admin
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'), 
    path('data-ajuan/', views.data_ajuan, name='data_ajuan'), 
    path('data-karyawan/', views.data_karyawan, name='data_karyawan'), 
    path('edit-data-karyawan/', views.edit_data_karyawan, name='edit_data_karyawan'), 
    path('detail-data-karyawan/', views.detail_data_karyawan, name='detail_data_karyawan'), 
    path('history/', views.history, name='history'),
    path('dataaccount/', views.data_akun, name='data_akun'),
    

    # karyawan
    path('dashboard/', views.dashboard_karyawan, name='dashboard_karyawan'),
]
