const body = document.body;
const button = document.getElementById("theme-toggle");

// Load saved theme
let savedTheme = localStorage.getItem("theme") || "dark";
body.classList.add(savedTheme);
updateButton(savedTheme);

button.addEventListener("click", () => {
    const current = body.classList.contains("dark") ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";

    body.classList.remove(current);
    body.classList.add(next);

    localStorage.setItem("theme", next);
    updateButton(next);
});

function updateButton(theme){
    button.textContent = theme === "dark"
        ? "☀️ Light"
        : "🌙 Dark";
}