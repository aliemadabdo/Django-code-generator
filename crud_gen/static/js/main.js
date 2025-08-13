// main.js
document.addEventListener("DOMContentLoaded", function () {
    const baseHomeUrl = "http://127.0.0.1:8000/"; // <-- Change to your actual IP:PORT if different
    const isHomePage =
        window.location.pathname === "/" ||
        window.location.pathname === "/home/"
        
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            const targetSection = this.getAttribute("data-target");

            if (!isHomePage) {
                // Redirect to actual home page with section hash
                e.preventDefault();
                window.location.href = `${baseHomeUrl}#${targetSection}`;
            } else {
                // Smooth scroll within the home page
                e.preventDefault();
                const section = document.getElementById(targetSection);
                if (section) {
                    section.scrollIntoView({ behavior: "smooth" });
                }
            }
        });
    });
});
