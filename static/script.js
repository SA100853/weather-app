function toggleTheme() {
    const html = document.documentElement;
    const current = html.dataset.theme;
    const newTheme = current === "dark" ? "light" : "dark";
    html.dataset.theme = newTheme;
    localStorage.setItem("theme", newTheme);
}

window.onload = () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.dataset.theme = savedTheme;
};
