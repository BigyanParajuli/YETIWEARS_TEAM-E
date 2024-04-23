// JavaScript to handle active class on click
document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
