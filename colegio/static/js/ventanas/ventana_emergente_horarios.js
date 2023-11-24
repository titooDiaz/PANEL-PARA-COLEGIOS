function mostrarVentana(modal) {
    console.log(modal)
    const ventana = document.getElementById(modal);
    ventana.classList.remove('hidden');
}

function cerrarVentana(modal) {
const ventana = document.getElementById(modal);
ventana.classList.add('hidden');
}