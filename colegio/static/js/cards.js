document.getElementById('dropdownButtonHorario').addEventListener('click', function() {
  var dropdown = document.getElementById('horario-dropdown');
  if (dropdown.classList.contains('hidden')) {
      dropdown.classList.remove('hidden');
  } else {
      dropdown.classList.add('hidden');
  }
});

document.getElementById('dropdownButtonGrados').addEventListener('click', function() {
  var dropdown = document.getElementById('grados-dropdown');
  if (dropdown.classList.contains('hidden')) {
      dropdown.classList.remove('hidden');
  } else {
      dropdown.classList.add('hidden');
  }
});

document.getElementById('dropdownButtonMaterias').addEventListener('click', function() {
  var dropdown = document.getElementById('materias-dropdown');
  if (dropdown.classList.contains('hidden')) {
      dropdown.classList.remove('hidden');
  } else {
      dropdown.classList.add('hidden');
  }
});

document.getElementById('dropdownButtonActividades').addEventListener('click', function() {
  var dropdown = document.getElementById('actividades-dropdown');
  if (dropdown.classList.contains('hidden')) {
      dropdown.classList.remove('hidden');
  } else {
      dropdown.classList.add('hidden');
  }
});