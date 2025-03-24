from django.shortcuts import render , redirect ,  redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Karyawan , KontakKaryawan,SuamiIstri , AnakKaryawan , DokumenKaryawan , RiwayatJabatan
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import JsonResponse
from datetime import date, datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



# API Data Karyawan
def api_karyawan(request):
    search_query = request.GET.get("search", "").strip()
    if search_query:
        karyawan_list = Karyawan.objects.filter(nama__icontains=search_query)[:10]
    else:
        karyawan_list = Karyawan.objects.all()[:10] 
    data = [{"id": karyawan.id, "text": karyawan.nama} for karyawan in karyawan_list]
    return JsonResponse({"results": data}, safe=False)

# Hitung Umur Otomatis
def hitung_umur(tanggal_lahir):
    if tanggal_lahir:
        today = date.today()
        lahir = datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()

        tahun = today.year - lahir.year
        bulan = today.month - lahir.month

        if bulan < 0:  
            tahun -= 1
            bulan += 12  

        return f"{tahun} Tahun {bulan} Bulan"
    return None

# Login
def login_admin(request):
    if request.user.is_authenticated:
        return redirect('dashboard_admin')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  
            user = authenticate(request, username=user.username, password=password)  
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_staff: 
            login(request, user)
            return redirect('dashboard_admin')
        else:
            messages.error(request, 'Email atau password salah atau Anda bukan admin.')

    return render(request, 'login.html')

# Logout
def logout_admin(request):
    logout(request)
    return redirect('login_admin')

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
@login_required
def dashboard_admin(request):
    return render(request, 'views/admin/dashboard_admin.html')
def data_ajuan(request):
    return render(request, 'views/admin/data_ajuan.html')

# Data karywan
def data_karyawan(request):
    data_karyawan = Karyawan.objects.all()
    return render(request, 'views/admin/data_karyawan.html', {'data_karyawan': data_karyawan})

# Hapus Data Karyawan
def hapus_karyawan(request, karyawan_id):
    if request.method == "POST":
        try:
            karyawan = Karyawan.objects.get(id=karyawan_id)
            karyawan.delete()
            return JsonResponse({"success": True, "message": "Karyawan berhasil dihapus"})
        except Karyawan.DoesNotExist:
            return JsonResponse({"success": False, "message": "Karyawan tidak ditemukan"})
    return JsonResponse({"success": False, "message": "Metode tidak diizinkan"}, status=405)

# Input Data Karyawan
@login_required
def input_data_karyawan(request):
    daftar_jabatan = [
        "Manager", "Supervisor", "Staff HRD", "Staff IT", "Staff Keuangan", "Staff Marketing"
    ]

   
    if request.method == "POST":
        try:
            # Ambil data dari form dan ubah ke huruf besar
            nama = request.POST.get("nama", "").strip().upper()
            jabatan = request.POST.get("jabatan", "").strip().upper()
            nik = request.POST.get("nik", "").strip()
            no_induk_karyawan = request.POST.get("no_induk_karyawan", "").strip()
            npwp = request.POST.get("npwp", "").strip()
            no_bpjs = request.POST.get("no_bpjs", "").strip()
            jenis_kelamin = request.POST.get("jenis_kelamin", "").strip()
            tempat_lahir = request.POST.get("tempat_lahir", "").strip()
            tanggal_lahir = request.POST.get("tanggal_lahir", "").strip() or None
            alamat = request.POST.get("alamat", "").strip()
            status_karyawan = request.POST.get("status_karyawan", "").strip()
            tanggal_masuk = request.POST.get("tanggal_masuk", "").strip()
            tanggal_keluar = request.POST.get("tanggal_keluar", "").strip() or None
            foto_profile = request.FILES.get("foto_profile")


            if Karyawan.objects.filter(nik=nik).exists():
                messages.error(request, "NIK sudah terdaftar, gunakan NIK lain!")
                return redirect("input_data_karyawan")
            
            if Karyawan.objects.filter(no_induk_karyawan=no_induk_karyawan).exists():
                messages.error(request, "No Induk Karyawan sudah terdaftar, gunakan yang lain!")
                return redirect("input_data_karyawan")

            if Karyawan.objects.filter(npwp=npwp).exists():
                messages.error(request, "NPWP sudah terdaftar, gunakan yang lain!")
                return redirect("input_data_karyawan")

            if Karyawan.objects.filter(no_bpjs=no_bpjs).exists():
                messages.error(request, "No BPJS sudah terdaftar, gunakan yang lain!")
                return redirect("input_data_karyawan")

            # Hitung umur otomatis
            umur = hitung_umur(tanggal_lahir)

            # Simpan data karyawan
            Karyawan.objects.create(
                nama=nama,
                jabatan=jabatan,
                nik=nik,
                no_induk_karyawan=no_induk_karyawan,
                npwp=npwp,
                no_bpjs=no_bpjs,
                jenis_kelamin=jenis_kelamin,
                tempat_lahir=tempat_lahir,
                tanggal_lahir=tanggal_lahir,
                umur=umur, 
                alamat=alamat,
                status_karyawan=status_karyawan,
                tanggal_masuk=tanggal_masuk,
                tanggal_keluar=tanggal_keluar,
                foto_profile=foto_profile
            )

            messages.success(request, "Data karyawan berhasil disimpan!")
            return redirect("data_karyawan")

        except IntegrityError:
            messages.error(request, "Terjadi kesalahan integritas data. Periksa kembali input Anda.")

    riwayat_jabatan = RiwayatJabatan.objects.select_related('karyawan').all().order_by('-tanggal_mulai')
   
    return render(request, "views/admin/input_data_karyawan.html", {
        "daftar_jabatan": daftar_jabatan,
        "riwayat_jabatan": riwayat_jabatan  # Tambahkan riwayat jabatan ke konteks
    })

# Input Data Kontak Karyawan
@login_required
def input_kontak_karyawan(request):
    storage = get_messages(request) 
    storage.used = True  

    karyawan_list = Karyawan.objects.all()
    context = {"karyawan_list": karyawan_list}

    if request.method == "POST":
        try:
            karyawan_id = request.POST.get("karyawan_kontak")
            if not karyawan_id:
                messages.error(request, "Pilih karyawan terlebih dahulu!")
                return render(request, "views/admin/input_kontak_karyawan.html", context)

            karyawan = Karyawan.objects.get(id=karyawan_id)

            email = request.POST.get("email", "").strip()
            no_telepon = request.POST.get("no_telepon", "").strip()
            instagram = request.POST.get("instagram", "").strip()
            facebook = request.POST.get("facebook", "").strip()
            twitter = request.POST.get("twitter", "").strip()

            if KontakKaryawan.objects.filter(email=email).exclude(karyawan=karyawan).exists():
                messages.error(request, "Email sudah digunakan oleh karyawan lain!")
            elif KontakKaryawan.objects.filter(no_telepon=no_telepon).exclude(karyawan=karyawan).exists():
                messages.error(request, "Nomor telepon sudah digunakan oleh karyawan lain!")
            else:
                KontakKaryawan.objects.update_or_create(
                    karyawan=karyawan,
                    defaults={
                        "email": email,
                        "no_telepon": no_telepon,
                        "instagram": instagram,
                        "facebook": facebook,
                        "twitter": twitter
                    }
                )
                messages.success(request, "Kontak karyawan berhasil disimpan!")

            context.update({
                "selected_karyawan": karyawan_id,
                "email": email,
                "no_telepon": no_telepon,
                "instagram": instagram,
                "facebook": facebook,
                "twitter": twitter
            })
            return render(request, "views/admin/input_data_karyawan.html", context)

        except Karyawan.DoesNotExist:
            messages.error(request, "Karyawan tidak ditemukan!")

    return render(request, "views/admin/input_data_karyawan.html", context)

# Input Suami Istri
@login_required
def input_suami_istri(request):
    karyawan_list = Karyawan.objects.all()

    if request.method == "POST":
        karyawan_id = request.POST.get("karyawan_suami")
        nama = request.POST.get("nama", "").strip().upper()
        tempat_lahir = request.POST.get("tempat_lahir", "").strip().upper()
        tanggal_lahir = request.POST.get("tanggal_lahir")
        pendidikan_terakhir = request.POST.get("pendidikan_terakhir")
        no_telp = request.POST.get("no_telp")
        foto = request.FILES.get("foto")

        # Validasi form tidak boleh kosong
        if not all([karyawan_id, nama, tempat_lahir, tanggal_lahir, pendidikan_terakhir, no_telp]):
            messages.error(request, "Harap isi semua data dengan benar!")
            return redirect(reverse("input_suami_istri"))

        # Validasi format tanggal
        try:
            tanggal_lahir = datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Format tanggal tidak valid! Gunakan format YYYY-MM-DD.")
            return redirect(reverse("input_suami_istri"))

        # Ambil objek karyawan atau tampilkan error jika tidak ditemukan
        karyawan = get_object_or_404(Karyawan, id=karyawan_id)

        # Cek apakah karyawan sudah memiliki data suami/istri
        if SuamiIstri.objects.filter(karyawan=karyawan).exists():
            messages.error(request, f"Karyawan {karyawan.nama} sudah memiliki data suami/istri!")
            return redirect(reverse("input_suami_istri"))

        # Simpan data ke database
        SuamiIstri.objects.create(
            karyawan=karyawan,
            nama=nama,
            tempat_lahir=tempat_lahir,
            tanggal_lahir=tanggal_lahir,
            pendidikan_terakhir=pendidikan_terakhir,
            no_telp=no_telp,
            foto_suami_istri=foto
        )
        messages.success(request, "Data Suami/Istri berhasil disimpan!")
        return redirect(reverse("input_suami_istri"))

    return render(request, "views/admin/input_data_karyawan.html", {"karyawan_list": karyawan_list})

# Input Data Anak
@login_required
def input_data_anak(request):
    karyawan_list = Karyawan.objects.all()
    jumlah_anak_options = range(1, 11) 

    if request.method == "POST":
     
        karyawan_id = request.POST.get("karyawan")
     
        if not karyawan_id:
            messages.error(request, "Pilih karyawan terlebih dahulu.")
            return redirect("input_data_anak")

        # Validasi karyawan
        karyawan = get_object_or_404(Karyawan, id=karyawan_id)

        # Ambil jumlah anak yang sudah terdaftar
        jumlah_anak_terdaftar = AnakKaryawan.objects.filter(karyawan=karyawan).count()
        jumlah_anak_baru = int(request.POST.get("jumlah_anak", 0))

        if jumlah_anak_baru < 1:
            messages.warning(request, "Jumlah anak harus minimal 1.")
            return redirect("input_data_anak")

        anak_baru_disimpan = 0  # Counter anak yang berhasil disimpan
        anak_ke_list = []  # List untuk menyimpan urutan anak yang baru ditambahkan

        for i in range(jumlah_anak_baru):
            nama = request.POST.get(f"nama_anak_{i}", "").strip().upper()
            tempat_lahir = request.POST.get(f"tempat_lahir_{i}", "").strip()
            tanggal_lahir = request.POST.get(f"tanggal_lahir_{i}", "")
            jenis_kelamin = request.POST.get(f"jenis_kelamin_{i}", "")
            no_telp = request.POST.get(f"no_telp_{i}", "").strip()
            status_anak = request.POST.get(f"status_anak_{i}", "Anak Kandung")  
            foto_anak = request.FILES.get(f"foto_anak_{i}")

            if not nama:
                continue  

            # Cek apakah anak dengan nama dan tanggal lahir ini sudah terdaftar untuk karyawan yang sama
            if AnakKaryawan.objects.filter(karyawan=karyawan, nama=nama, tanggal_lahir=tanggal_lahir).exists():
                messages.warning(request, f"Anak '{nama}' sudah terdaftar sebelumnya.")
                continue

            # Tentukan anak ke berapa (urutan)
            anak_ke = jumlah_anak_terdaftar + anak_baru_disimpan + 1

            # Buat entri baru untuk anak
            AnakKaryawan.objects.create(
                karyawan=karyawan,
                anak_ke=anak_ke,
                nama=nama,
                tempat_lahir=tempat_lahir,
                tanggal_lahir=tanggal_lahir,
                jenis_kelamin=jenis_kelamin,
                no_telp=no_telp,
                status_anak=status_anak,  
                foto_anak=foto_anak
            )

            anak_ke_list.append(f"{nama} (Anak ke-{anak_ke})")
            anak_baru_disimpan += 1

        if anak_baru_disimpan > 0:
            anak_ke_text = ", ".join(anak_ke_list)
            messages.success(request, f"{anak_baru_disimpan} anak baru berhasil disimpan untuk {karyawan.nama}: {anak_ke_text}.")
        else:
            messages.warning(request, "Tidak ada anak baru yang berhasil ditambahkan.")

        return redirect("input_data_anak")

    context = {
        "karyawan_list": karyawan_list,
        "jumlah_anak_options": jumlah_anak_options,
    }

    return render(request, "views/admin/input_data_karyawan.html", context)

# Input Dokumen Profile
@login_required
def input_dokumen(request):
    karyawan_list = Karyawan.objects.all()

    if request.method == "POST":
        karyawan_id = request.POST.get("karyawan")

        if not karyawan_id:
            messages.error(request, "Pilih karyawan terlebih dahulu.")
            return redirect("input_dokumen")

        karyawan = get_object_or_404(Karyawan, id=karyawan_id)

        # Cek apakah karyawan sudah memiliki dokumen
        if DokumenKaryawan.objects.filter(karyawan=karyawan).exists():
            messages.warning(request, f"Dokumen untuk {karyawan.nama} sudah pernah diunggah dan tidak bisa ditambahkan lagi.")
            return redirect("input_dokumen")

        kartu_keluarga = request.FILES.get("kartu_keluarga")
        ktp = request.FILES.get("ktp")
        dokumen_sk = request.FILES.get("dokumen_sk")

        # Buat dokumen baru
        DokumenKaryawan.objects.create(
            karyawan=karyawan,
            kartu_keluarga=kartu_keluarga,
            ktp=ktp,
            dokumen_sk=dokumen_sk
        )

        messages.success(request, f"Dokumen untuk {karyawan.nama} berhasil disimpan!")
        return redirect("input_dokumen")

    return render(request, "views/admin/input_data_karyawan.html", {
        "karyawan_list": karyawan_list,
    })

# Input Data Riwayat Jabatan
def data_riwayat_jabatan(request):
    data_riwayat_jabatan = RiwayatJabatan.objects.all().order_by("-tanggal_mulai")  # Urutkan dari terbaru
    karyawan_list = Karyawan.objects.all()
    

    daftar_jabatan = ["Manager", "Supervisor", "Staff", "Admin", "HRD", "IT Support"]

    if request.method == "POST":
        karyawan_id = request.POST.get("karyawan")
        jabatan = request.POST.get("jabatan")
        no_sk = request.POST.get("no_sk")
        dokumen_sk = request.FILES.get("dokumen_sk")
        tanggal_mulai = request.POST.get("tanggal_mulai")
        tanggal_akhir = request.POST.get("tanggal_akhir")

        if not karyawan_id:
            messages.error(request, "Pilih karyawan terlebih dahulu.")
            return redirect("data_riwayat_jabatan")

        karyawan = get_object_or_404(Karyawan, id=karyawan_id)

        jabatan_aktif = RiwayatJabatan.objects.filter(karyawan=karyawan, tanggal_akhir__isnull=True).exists()
        if jabatan_aktif and not tanggal_akhir:
            messages.error(request, f"{karyawan.nama} masih memiliki jabatan aktif!")
            return redirect("data_riwayat_jabatan")

        if RiwayatJabatan.objects.filter(no_sk=no_sk).exists():
            messages.error(request, "Nomor SK sudah digunakan, gunakan nomor lain!")
            return redirect("data_riwayat_jabatan")

        try:
            tanggal_mulai = date.fromisoformat(tanggal_mulai)
            if tanggal_akhir:
                tanggal_akhir = date.fromisoformat(tanggal_akhir)
                if tanggal_mulai > tanggal_akhir:
                    messages.error(request, "Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
                    return redirect("data_riwayat_jabatan")
            else:
                tanggal_akhir = None
        except ValueError:
            messages.error(request, "Format tanggal tidak valid!")
            return redirect("data_riwayat_jabatan")

        RiwayatJabatan.objects.create(
            karyawan=karyawan,
            jabatan=jabatan,
            no_sk=no_sk,
            dokumen_sk=dokumen_sk,
            tanggal_mulai=tanggal_mulai,
            tanggal_akhir=tanggal_akhir,
        )

        messages.success(request, f"Riwayat jabatan untuk {karyawan.nama} berhasil disimpan!")
        return redirect("data_riwayat_jabatan")

    return render(request, "views/admin/form_riwayat/data_riwayat_jabatan.html", {
        "karyawan_list": karyawan_list,
        "data_riwayat_jabatan": data_riwayat_jabatan,
        "daftar_jabatan": daftar_jabatan, 

    })

# Edit Data Jabatan
def edit_riwayat_jabatan(request, id):
    if request.method == "POST":
        try:
            riwayat = RiwayatJabatan.objects.get(id=id)

            karyawan_id = request.POST.get("karyawan")
            jabatan = request.POST.get("jabatan")
            no_sk = request.POST.get("no_sk")
            tanggal_mulai = request.POST.get("tanggal_mulai")
            tanggal_akhir = request.POST.get("tanggal_akhir", None)

            # Pastikan format tanggal valid
            try:
                tanggal_mulai = datetime.strptime(tanggal_mulai, "%Y-%m-%d").date() if tanggal_mulai else None
                tanggal_akhir = datetime.strptime(tanggal_akhir, "%Y-%m-%d").date() if tanggal_akhir else None
            except ValueError:
                return JsonResponse({"success": False, "message": "Format tanggal tidak valid"}, status=400)

            riwayat.karyawan_id = karyawan_id
            riwayat.jabatan = jabatan
            riwayat.no_sk = no_sk
            riwayat.tanggal_mulai = tanggal_mulai
            riwayat.tanggal_akhir = tanggal_akhir

            riwayat.save()

            return JsonResponse({"success": True, "message": "Data berhasil diperbarui."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Terjadi kesalahan: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Metode tidak diizinkan"}, status=405)


# Hapus Data Riwayat Jabatan
@csrf_exempt
def hapus_riwayat_jabatan(request, id):
    if request.method == "DELETE":
        try:
            riwayat = RiwayatJabatan.objects.get(id=id)
            riwayat.delete()
            return JsonResponse({"success": True})
        except RiwayatJabatan.DoesNotExist:
            return JsonResponse({"success": False, "error": "Data tidak ditemukan"})
    return JsonResponse({"success": False, "error": "Metode tidak diizinkan"})

def edit_data_karyawan(request):
    return render(request, 'views/admin/edit_data_karyawan.html')
def detail_data_karyawan(request):
    return render(request, 'views/admin/detail_data_karyawan.html')
def history(request):
    return render(request, 'views/admin/history.html')
def data_akun(request):
    return render(request, 'views/admin/data_akun.html')

# Modal Admin Riwayat Profile2
def modal_riwayat_jabatan(request):
    return render(request, 'views/admin/form_riwayat/input_riwayat_jabatan.html')
def modal_riwayat_pendidikan(request):
    return render(request, 'views/admin/form_riwayat/input_riwayat_pendidikan.html')
def modal_riwayat_non_formal(request):
    return render(request, 'views/admin/form_riwayat/input_riwayat_non_formal.html')
def modal_riwayat_prestasi(request):
    return render(request, 'views/admin/form_riwayat/input_riwayat_prestasi.html')
def modal_riwayat_pelanggaran(request):
    return render(request, 'views/admin/form_riwayat/input_riwayat_pelanggaran.html')

# karyawan
def dashboard_karyawan(request):
    return render(request, 'views/karyawan/dashboard_karyawan.html')