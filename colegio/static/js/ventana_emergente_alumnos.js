
  function mostrarVentana() {
          const ventana = document.getElementById('EmergenteAlumnos');
          ventana.classList.remove('hidden');
      }

  function cerrarVentana() {
      const ventana = document.getElementById('EmergenteAlumnos');
      ventana.classList.add('hidden');
  }