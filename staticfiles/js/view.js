function makeBgGrey(x) {
    x.style.backgroundColor = "#808080"
}
function normalBg(x) {
    x.style.backgroundColor = "#F5F5F5"
}
document.querySelectorAll(".files_list_text").forEach(i => {
    i.setAttribute("onmouseover", "makeBgGrey(this)")
    i.setAttribute("onmouseout", "normalBg(this)")
});