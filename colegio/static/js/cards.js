document.addEventListener("DOMContentLoaded", function() {
  const botones = document.querySelectorAll(".cardButton");
  const botonDropdown = document.querySelector("[id='ajuste-dropdown']");
  
  let menuAbierto = false;
  document.addEventListener("click", function(event) {         
    if (menuAbierto) {
        botonDropdown.style.display = "none";
      menuAbierto = false;   
    }
  }),

  botones.forEach(function(boton) {
    const mirar = botonDropdown.querySelector('#mirar-dropdown');    
    const editar = botonDropdown.querySelector('#editar-dropdown');

    boton.addEventListener("click", function(event) {
      const dataUrlVer =  boton.getAttribute('data-url-ver');
      const dataUrlEditar =  boton.getAttribute('data-url-editar');
      mirar.setAttribute('href', dataUrlVer);
      editar.setAttribute('href', dataUrlEditar);
      event.stopPropagation();
    })

    boton.addEventListener("click", function(event) {
      event.stopPropagation
      const rect = boton.getBoundingClientRect();
      const top = rect.top + 30;
      const left = rect.left;

      botonDropdown.style.position = "absolute";
      botonDropdown.style.display = "block";
      botonDropdown.style.top = top + "px";
      botonDropdown.style.left = left + "px"; 
      menuAbierto = true;
    });
  });
});