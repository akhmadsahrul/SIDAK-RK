from django.db import models
from datetime import date

# Model Karyawan
class Karyawan(models.Model):
    STATUS_KARYAWAN = [
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    ]
    
    JENIS_KELAMIN = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]
   
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=100)
    nik = models.CharField(max_length=20, unique=True)
    no_induk_karyawan = models.CharField(max_length=50, unique=True)
    npwp = models.CharField(max_length=30, blank=True, null=True)
    no_bpjs = models.CharField(max_length=30, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=15, choices=JENIS_KELAMIN)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(blank=True, null=True) 
    umur = models.CharField(max_length=50, null=True, blank=True) 
    alamat = models.TextField()
    status_karyawan = models.CharField(max_length=15, choices=STATUS_KARYAWAN, default='Aktif')
    tanggal_masuk = models.DateField()
    tanggal_keluar = models.DateField(blank=True, null=True)
    foto_profile = models.ImageField(upload_to='img/profile/', blank=True, null=True)

    def __str__(self):
        return self.nama

# Model Informasi Kontak Karyawan
class KontakKaryawan(models.Model):
    karyawan = models.OneToOneField(Karyawan, on_delete=models.CASCADE)
    email = models.EmailField()
    no_telepon = models.CharField(max_length=20)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Kontak {self.karyawan.nama}"

# Model Data Suami/Istri
class SuamiIstri(models.Model):

    foto_suami_istri = models.FileField(upload_to="img/profile_suami_istri/", blank=True, null=True)
    karyawan = models.OneToOneField("Karyawan", on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(null=False, blank=False)
    pendidikan_terakhir = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=20)

    def __str__(self):
        return f"Pasangan {self.karyawan.nama}"

# Model Data Anak
class AnakKaryawan(models.Model):
    JENIS_KELAMIN = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]

    karyawan = models.ForeignKey(
        Karyawan, on_delete=models.CASCADE, related_name="anak_list"
    )
    anak_ke = models.PositiveIntegerField(default=1)  
    nama = models.CharField(max_length=255)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=15, choices=JENIS_KELAMIN)
    status_anak = models.CharField(max_length=50, default="Tidak diketahui")  # Tambah default
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    foto_anak = models.ImageField(upload_to='img/foto_anak/', blank=True, null=True)

    class Meta:
        unique_together = ('karyawan', 'nama', 'tanggal_lahir')
        ordering = ['anak_ke']

    def __str__(self):
        return f"{self.karyawan.nama} - {self.nama} (Anak ke-{self.anak_ke})"



# Model Dokumen Karyawan
class DokumenKaryawan(models.Model):
    karyawan = models.OneToOneField(Karyawan, on_delete=models.CASCADE)
    kartu_keluarga = models.FileField(upload_to='dokumen/kartu_keluarga/', blank=True, null=True)
    ktp = models.FileField(upload_to='dokumen/ktp/', blank=True, null=True)
    dokumen_sk = models.FileField(upload_to='dokumen/sk/', blank=True, null=True)

    def __str__(self):
        return f"Dokumen {self.karyawan.nama}"
    

# Model Riwayat Jabatan
class RiwayatJabatan(models.Model):
    karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE, related_name="riwayat_jabatan")
    jabatan = models.CharField(max_length=100)
    no_sk = models.CharField(max_length=50, unique=True)  
    dokumen_sk = models.FileField(upload_to="dokumen/riwayat_jabatan/", blank=True, null=True)
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField(blank=True, null=True)  

    class Meta:
        ordering = ["-tanggal_mulai"] 

    def __str__(self):
        return f"{self.karyawan.nama} - {self.jabatan} ({self.tanggal_mulai} - {self.tanggal_akhir or 'Sekarang'})"

    @property
    def masa_jabatan(self):
        """Menghitung masa jabatan dalam tahun dan bulan"""
        akhir = self.tanggal_akhir if self.tanggal_akhir else date.today()
        delta = akhir - self.tanggal_mulai
        tahun = delta.days // 365
        bulan = (delta.days % 365) // 30
        return f"{tahun} tahun {bulan} bulan" if tahun or bulan else "Kurang dari 1 bulan"
