function showSection(section) {
    // Ocultar todas las secciones
    document.querySelectorAll('[id^="content_schedule"] > div').forEach(div => div.classList.add('hidden'));
    
    // Mostrar la sección seleccionada
    // show the select section
    document.getElementById(section).classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // Desplazar al elemento de ancla
    document.getElementById('top').scrollIntoView({ behavior: 'smooth' });


}