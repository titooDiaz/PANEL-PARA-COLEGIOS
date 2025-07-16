function mostrarVentana(modal, pk) {
    const ventana = document.getElementById(modal+pk);
    ventana.classList.remove('hidden');
}

function cerrarVentana(modal,pk) {
const ventana = document.getElementById(modal+pk);
ventana.classList.add('hidden');
}