document.addEventListener("DOMContentLoaded", function () {
    const jumlahAnakSelect = document.getElementById("jumlahAnak");
    const anakContainer = document.getElementById("anakContainer");

    if (!jumlahAnakSelect || !anakContainer) {
        console.error("Error: Elemen jumlahAnak atau anakContainer tidak ditemukan.");
        return;
    }

    // Ambil data-status-anak dari atribut div
    let statusAnakData = anakContainer.getAttribute("data-status-anak");
    let statusAnakOptions = [];

    if (statusAnakData) {
        try {
            statusAnakOptions = JSON.parse(statusAnakData);
        } catch (error) {
            console.error("Error parsing JSON data-status-anak:", error);
        }
    }

    // Jika data-status-anak tidak tersedia atau parsing gagal, gunakan default options
    if (statusAnakOptions.length === 0) {
        statusAnakOptions = ["Anak Kandung", "Anak Angkat", "Lainnya"];
    }



    function generateForm(index) {
        let statusOptionsHTML = statusAnakOptions
            .map(status => `<option value="${status}">${status}</option>`)
            .join("");

        return `
            <div class="border p-3 mb-3 rounded" id="formAnak${index}">
                <h6 class="fw-bold">Anak Ke-${index + 1}</h6>
                <div class="row g-3">
                    <div class="d-flex flex-column align-items-center position-relative">
                        <img id="previewAnak${index}" src="/static/img/default_anak.png" 
                            alt="Foto Anak" class="rounded-circle border shadow-sm" 
                            style="width: 150px; height: 150px; object-fit: cover;">

                        <input type="file" name="foto_anak_${index}" id="fileAnak${index}" accept="image/*" class="d-none">
                        
                        <label for="fileAnak${index}" class="btn btn-light btn-sm position-absolute" 
                            style="bottom: 10px; right: 10px; padding: 8px;">
                            <i class="fas fa-edit fs-5 text-dark"></i> Edit Foto
                        </label>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Nama</label>
                        <input type="text" name="nama_anak_${index}" class="form-control" required oninput="this.value = this.value.toUpperCase()">
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Tempat Lahir</label>
                        <input type="text" name="tempat_lahir_${index}" class="form-control" required oninput="this.value = this.value.toUpperCase()">
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Tanggal Lahir</label>
                        <input type="date" name="tanggal_lahir_${index}" class="form-control" required>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Jenis Kelamin</label>
                        <select name="jenis_kelamin_${index}" class="form-control" required>
                            <option value="Laki-laki">Laki-laki</option>
                            <option value="Perempuan">Perempuan</option>
                        </select>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">No Telp.</label>
                        <input type="number" name="no_telp_${index}" class="form-control">
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Status</label>
                        <select name="status_anak_${index}" class="form-control" required>
                            ${statusOptionsHTML}
                        </select>
                    </div>
                </div>
            </div>`;
    }

    function updateForms() {
        const jumlahAnak = parseInt(jumlahAnakSelect.value) || 1;
        anakContainer.innerHTML = ""; // Kosongkan form sebelumnya

        for (let i = 0; i < jumlahAnak; i++) {
            anakContainer.insertAdjacentHTML("beforeend", generateForm(i));
        }

        // Tambahkan event listener untuk preview gambar setelah form dibuat
        for (let i = 0; i < jumlahAnak; i++) {
            const fileInput = document.getElementById(`fileAnak${i}`);
            const previewImg = document.getElementById(`previewAnak${i}`);

            if (fileInput && previewImg) {
                fileInput.addEventListener("change", function (event) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function (e) {
                            previewImg.src = e.target.result;
                        };
                        reader.readAsDataURL(file);
                    }
                });
            }
        }
    }

    // Set default 1 form anak saat halaman pertama kali dimuat
    updateForms();

    // Update form saat dropdown berubah
    jumlahAnakSelect.addEventListener("change", updateForms);
});
