const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('archivo');

// Prevenir comportamientos por defecto para eventos de arrastrar y soltar
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Añadir efectos visuales cuando se arrastra un archivo
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('border-blue-500'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('border-blue-500'), false);
});

// Manejar el evento "drop"
dropArea.addEventListener('drop', handleDrop, false);

//SUBIDO MEDIANTE UN DROP!
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    fileInput.files = files;  // Asignar los archivos al input de tipo file
    console.log("Archivo cargado en el formulario:", fileInput.files[0]);  // Opcional: ver el archivo en la consola
}

// SUBIDO MANUALMNTE
fileInput.addEventListener('change', function() {
    const files = fileInput.files;
    if (files.length > 0) {
        console.log("Archivo seleccionado:", files[0]);  // Muestra el nombre del archivo seleccionado
    }
});