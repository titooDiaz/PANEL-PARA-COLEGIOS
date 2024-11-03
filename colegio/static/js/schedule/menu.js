
function showSection(section) {
    // Ocultar todas las secciones
    document.querySelectorAll('[id^="content_schedule"] > div').forEach(div => div.classList.add('hidden'));
    
    // Mostrar la sección seleccionada
    document.getElementById(section).classList.remove('hidden');
}
