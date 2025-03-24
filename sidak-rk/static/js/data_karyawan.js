//Hover Tab pada data
document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-tabs .nav-link");
    const tabContents = document.querySelectorAll(".tab-content");

    navLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            // Hapus 'active' dari semua tab
            navLinks.forEach(nav => nav.classList.remove("active"));
            this.classList.add("active");

            // Sembunyikan semua tab-content
            tabContents.forEach(content => content.classList.remove("active"));

            // Tampilkan tab yang sesuai
            const target = this.getAttribute("data-target");
            document.getElementById(target).classList.add("active");
        });
    });
});


// untuk Foto Profile
document.getElementById('profileutama').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profileImage').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});
// Untuk profile data Suami
document.getElementById('profiledatasuami').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profildatasuami').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});
// untuk profile data anak
document.getElementById('profiledataanak').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profildataanak').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});
