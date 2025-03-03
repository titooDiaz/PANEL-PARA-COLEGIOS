document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".mask-icon").forEach(el => {
        const iconUrl = el.getAttribute("data-icon");
        el.style.webkitMaskImage = `url('${iconUrl}')`;
        el.style.maskImage = `url('${iconUrl}')`;
    });
});