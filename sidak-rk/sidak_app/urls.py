from django.urls import path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import logout_admin, api_karyawan, hapus_riwayat_jabatan,edit_riwayat_jabatan 

urlpatterns = [
    # login
    path('', views.login_admin, name='login_admin'), 
    path('logout/', logout_admin, name='logout_admin'),
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

    # Input Identitas Profile 1
    path('input-data-karyawan/', views.input_data_karyawan, name='input_data_karyawan'), 
    path('input-kontak/', views.input_kontak_karyawan, name='input_kontak_karyawan'), 
    path('input-suami-istri/', views.input_suami_istri, name='input_suami_istri'), 
    path('input-data-anak/', views.input_data_anak, name='input_data_anak'),
    path('input-dokumen/', views.input_dokumen, name='input_dokumen'),
    
    # Riwayat Jabatan
    path('data-riwayat-jabatan/', views.data_riwayat_jabatan, name='data_riwayat_jabatan'),
    path("hapus-riwayat-jabatan/<int:id>/", hapus_riwayat_jabatan, name="hapus_riwayat_jabatan"),
    path('edit-riwayat-jabatan/<int:id>/', edit_riwayat_jabatan, name="edit_riwayat_jabatan"),


    # Forms Riawayat Input Data Karyawan
    path('input-riwayat-jabatan/', views.modal_riwayat_jabatan, name='modal_riwayat_jabatan'),
    path('input-riwayat-pendidikan/', views.modal_riwayat_pendidikan, name='modal_riwayat_pendidikan'),
    path('input-riwayat-pendidikan-non-formal/', views.modal_riwayat_non_formal, name='modal_riwayat_non_formal'),
    path('input-riwayat-prestasi/', views.modal_riwayat_prestasi, name='modal_riwayat_prestasi'),
    path('input-riwayat-pelanggaran/', views.modal_riwayat_pelanggaran, name='modal_riwayat_pelanggaran'),

    path('detail-data-karyawan/', views.detail_data_karyawan, name='detail_data_karyawan'), 
    path('history/', views.history, name='history'),
    path('dataaccount/', views.data_akun, name='data_akun'),
    
    # API Data  Karyawan
    path('api/karyawan/', api_karyawan, name='api-karyawan'),
    # Hapus Data Karyawan
    path('hapus-karyawan/<int:karyawan_id>/', views.hapus_karyawan, name='hapus_karyawan'),

    # Dashboard karyawan
    path('dashboard/', views.dashboard_karyawan, name='dashboard_karyawan'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
