function mostrarVentanaHorarios(modal, pk) {
    const ventana = document.getElementById(modal+pk);
    ventana.classList.remove('hidden');
}

function cerrarVentanaHorarios(modal,pk) {
const ventana = document.getElementById(modal+pk);
ventana.classList.add('hidden');
}