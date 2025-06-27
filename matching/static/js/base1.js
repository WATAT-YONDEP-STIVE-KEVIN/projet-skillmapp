
function toggleMenu() {
    document.getElementById("main-nav").classList.toggle("active");
}
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    const mode = document.body.classList.contains("dark-mode") ? "dark" : "light";
    localStorage.setItem("mode", mode);
}
