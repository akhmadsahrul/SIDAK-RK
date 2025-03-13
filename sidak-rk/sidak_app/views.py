from django.shortcuts import render


# Login
def login(request):
    return render(request, 'login.html')

# Login
def ubah_katasandi(request):
    return render(request, 'ubah_kata_sandi.html')

# Forgot Password
def forgotpassword(request):
    return render(request, 'forgotpassword.html')
def verify(request):
    return render(request, 'verify.html')
def resetpassword(request):
    return render(request, 'resetpassword.html')
def setnew(request):
    return render(request, 'setnew.html')

# admin
def dashboard_admin(request):
    return render(request, 'views/admin/dashboard_admin.html')
def data_ajuan(request):
    return render(request, 'views/admin/data_ajuan.html')
def data_karyawan(request):
    return render(request, 'views/admin/data_karyawan.html')
def edit_data_karyawan(request):
    return render(request, 'views/admin/edit_data_karyawan.html')
def detail_data_karyawan(request):
    return render(request, 'views/admin/detail_data_karyawan.html')
def history(request):
    return render(request, 'views/admin/history.html')
def data_akun(request):
    return render(request, 'views/admin/data_akun.html')

# karyawan
def dashboard_karyawan(request):
    return render(request, 'views/karyawan/dashboard_karyawan.html')