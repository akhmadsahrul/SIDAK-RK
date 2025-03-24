document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-hapus").forEach(button => {
        button.addEventListener("click", function () {
            let karyawanId = this.getAttribute("data-id");

            Swal.fire({
                title: "Apakah Anda yakin?",
                text: "Data karyawan akan dihapus secara permanen!",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Ya, Hapus!"
            }).then((result) => {
                if (result.isConfirmed) {
                    let csrfTokenElement = document.querySelector("#csrfToken");
                    if (!csrfTokenElement) {
                        Swal.fire("Error!", "CSRF token tidak ditemukan!", "error");
                        return;
                    }
                    let csrfToken = csrfTokenElement.value;

                    fetch(`/hapus-karyawan/${karyawanId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken,
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire(
                                "Terhapus!",
                                "Data karyawan berhasil dihapus.",
                                "success"
                            );

                            // Hapus baris tabel setelah data berhasil dihapus
                            document.querySelector(`tr[data-id='${karyawanId}']`).remove();
                        } else {
                            Swal.fire("Gagal!", data.message, "error");
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        Swal.fire("Error!", "Terjadi kesalahan saat menghapus data.", "error");
                    });
                }
            });
        });
    });
});