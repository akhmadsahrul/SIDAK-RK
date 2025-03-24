// Filter Pagination And Search 
document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("dataTable");
    const rows = Array.from(table.getElementsByTagName("tbody")[0].getElementsByTagName("tr"));
    const searchInput = document.getElementById("searchInput");
    const entriesSelect = document.getElementById("entries");
    const pagination = document.getElementById("pagination");
    const tableInfo = document.getElementById("tableInfo");

    let currentPage = 1;
    let rowsPerPage = parseInt(entriesSelect.value);

    function displayTable() {
        let searchText = searchInput.value.toLowerCase();
        let filteredRows = rows.filter(row => row.innerText.toLowerCase().includes(searchText));

        let totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        currentPage = Math.min(currentPage, totalPages) || 1;

        let start = (currentPage - 1) * rowsPerPage;
        let end = start + rowsPerPage;

        rows.forEach(row => row.style.display = "none");
        filteredRows.slice(start, end).forEach(row => row.style.display = "table-row");

        tableInfo.innerText =
            `Menampilkan ${start + 1} - ${Math.min(end, filteredRows.length)} dari ${filteredRows.length} data`;
        updatePagination(totalPages);
    }

    function updatePagination(totalPages) {
        pagination.innerHTML = "";

        // Tombol "Sebelumnya"
        let prevLi = document.createElement("li");
        prevLi.className = `page-item ${currentPage === 1 ? "disabled" : ""}`;
        prevLi.innerHTML = `<a class="page-link" href="#"><i class="fa fa-chevron-left"></i></a>`;
        prevLi.addEventListener("click", function (e) {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                displayTable();
            }
        });
        pagination.appendChild(prevLi);

        // Nomor Halaman
        for (let i = 1; i <= totalPages; i++) {
            let li = document.createElement("li");
            li.className = `page-item ${i === currentPage ? "active" : ""}`;
            li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            li.addEventListener("click", function (e) {
                e.preventDefault();
                currentPage = i;
                displayTable();
            });
            pagination.appendChild(li);
        }

        // Tombol "Selanjutnya"
        let nextLi = document.createElement("li");
        nextLi.className = `page-item ${currentPage === totalPages ? "disabled" : ""}`;
        nextLi.innerHTML = `<a class="page-link" href="#"><i class="fa fa-chevron-right"></i></a>`;
        nextLi.addEventListener("click", function (e) {
            e.preventDefault();
            if (currentPage < totalPages) {
                currentPage++;
                displayTable();
            }
        });
        pagination.appendChild(nextLi);
    }

    searchInput.addEventListener("input", function () {
        currentPage = 1;
        displayTable();
    });

    entriesSelect.addEventListener("change", function () {
        rowsPerPage = parseInt(this.value);
        currentPage = 1;
        displayTable();
    });

    displayTable();
});

// Sweet Alert Hapus Data Jabatan
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".btn-delete");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            let id = this.getAttribute("data-id");

            // Konfirmasi SweetAlert tanpa teks tambahan
            Swal.fire({
                title: "Anda Yakin Hapus Data Jabatan?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Iya",
                cancelButtonText: "Batal"
            }).then((result) => {
                if (result.isConfirmed) {
                    // Kirim request hapus ke server
                    fetch(`/hapus-riwayat-jabatan/${id}/`, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire("Dihapus!", "Data berhasil dihapus.", "success")
                                .then(() => location.reload()); 
                        } else {
                            Swal.fire("Gagal!", "Gagal menghapus data.", "error");
                        }
                    })
                    .catch(error => {
                        Swal.fire("Error!", "Terjadi kesalahan.", "error");
                        console.error("Error:", error);
                    });
                }
            });
        });
    });

    // Fungsi untuk mendapatkan CSRF token Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                let trimmed = cookie.trim();
                if (trimmed.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }
});

// Edit Pada Data Jabatan
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".btn-edit");
    const editModalElement = document.getElementById("editModal");
    const editModal = new bootstrap.Modal(editModalElement);
    const editForm = document.getElementById("editForm");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            let id = this.getAttribute("data-id");
            let karyawan = this.getAttribute("data-karyawan");
            let jabatan = this.getAttribute("data-jabatan");
            let noSk = this.getAttribute("data-no_sk");
            let tanggalMulai = this.getAttribute("data-tanggal_mulai");
            let tanggalAkhir = this.getAttribute("data-tanggal_akhir");

            document.getElementById("editId").value = id;
            document.getElementById("editKaryawan").value = karyawan;
            document.getElementById("editJabatan").value = jabatan;
            document.getElementById("editNoSk").value = noSk;

            document.getElementById("editTanggalMulai").value = tanggalMulai ? tanggalMulai : "";
            document.getElementById("editTanggalAkhir").value = tanggalAkhir ? tanggalAkhir : "";

            editModal.show();
        });
    });

    // Submit Edit Form
    editForm.addEventListener("submit", function (e) {
        e.preventDefault();

        let id = document.getElementById("editId").value;
        let formData = new FormData(this);

        fetch(`/edit-riwayat-jabatan/${id}/`, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire("Berhasil!", data.message, "success").then(() => {
                    editModal.hide();
                    location.reload();
                });
            } else {
                Swal.fire("Gagal!", data.message, "error");
            }
        })
        .catch(error => {
            console.error("Fetch Error:", error);
            Swal.fire("Error!", "Terjadi kesalahan pada server.", "error");
        });
    });

    // Fungsi untuk mendapatkan CSRF token Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                let trimmed = cookie.trim();
                if (trimmed.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }
});
