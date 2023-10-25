document.addEventListener("DOMContentLoaded", function() {
    const botones = document.querySelectorAll(".cardButton");
    const botonesDropdowns = document.getElementById('ajuste-dropdown')
  
    let menuAbierto = false;
  
    document.addEventListener("click", function(event) {
      if (menuAbierto) {
        botonesDropdowns.style.display = "none";
        menuAbierto = false;
      }
    });
  
    botones.forEach(function(boton, index) {
      boton.addEventListener("click", function(event) {
        event.stopPropagation();
        const rect = boton.getBoundingClientRect();
        const offsetVertical = 30;
  
        // Cerrar todos los menús desplegables
            botonesDropdowns.style.display = "none";
  
        const mirar = botonesDropdowns.querySelector('#mirar-dropdown');
        const editar = botonesDropdowns.querySelector('#editar-dropdown');
  
        // Recuperar la URL del atributo data-url
        const dataUrl = mirar.getAttribute('data-url');
  
        // Asignar la URL al enlace "Mirar"
        mirar.setAttribute('href', dataUrl);
  
        // Asignar la URL al enlace "Editar" si es necesario
        editar.setAttribute('href', 'Editar');
  
        const top = rect.top + offsetVertical;
        const left = rect.left;
  
        botonesDropdowns.style.position = "absolute";
        botonesDropdowns.style.display = "block";
        botonesDropdowns.style.top = top + "px";
        botonesDropdowns.style.left = left + "px";
  
        menuAbierto = true;
      });
    });
  });