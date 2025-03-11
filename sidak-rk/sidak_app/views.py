from django.shortcuts import render


# Login
def login(request):
    return render(request, 'login.html')
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
def history(request):
    return render(request, 'views/admin/history.html')

# karyawan
def dashboard_karyawan(request):
    return render(request, 'views/karyawan/dashboard_karyawan.html')