//BOTON SALIR
const mostrarVentanaBtn = document.getElementById("mostrarVentana");
const ventanaEmergente = document.getElementById("ventanaEmergente");
const cerrarVentanaBtn = document.getElementById("cerrarVentana");

mostrarVentanaBtn.addEventListener("click", () => {
    ventanaEmergente.classList.remove("hidden");
});

cerrarVentanaBtn.addEventListener("click", () => {
    ventanaEmergente.classList.add("hidden");
});


//USER
document.addEventListener("DOMContentLoaded", function() {
    const userMenuButton = document.getElementById("user-menu-button");
    const userDropdown = document.getElementById("user-dropdown");

    userMenuButton.addEventListener("click", function(event) {
        event.stopPropagation();
        userDropdown.classList.toggle("fixed");

        if (!userDropdown.classList.contains("fixed")) {
            userDropdown.style.display = "none";
        } else {
            userDropdown.style.display = "block";
        }
    });
    //cic afuera
    document.addEventListener("click", function(event) {
        if (userDropdown.classList.contains("fixed") && !userDropdown.contains(event.target)) {
            // Cerramos el menú
            userDropdown.classList.remove("fixed");
            userDropdown.style.display = "none";
        }
    });
});