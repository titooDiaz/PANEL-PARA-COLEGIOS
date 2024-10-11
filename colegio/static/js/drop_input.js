const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('archivo');
const filesList = document.getElementById('files_list'); // lista de archivos subidos

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

    // Crear un elemento HTML e insertarlo en el DOM
    const div = document.createElement('div');
    div.innerHTML = `<div class="p-4 flex w-full bg-green-400 rounded-lg my-4">
                        <div><i class="fa-solid fa-file"></i></div>
                        <div class="ml-4">${files[0].name}</div>
                    </div>`;
    
    filesList.appendChild(div);
}

// SUBIDO MANUALMNTE
fileInput.addEventListener('change', function() {
    const files = fileInput.files;
    if (files.length > 0) {
        console.log("Archivo seleccionado:", files[0]);  // Muestra el nombre del archivo seleccionado
    }

    // Crear un elemento HTML e insertarlo en el DOM
    const div = document.createElement('div');
    div.innerHTML = `
                    <div class="p-4 flex w-full bg-green-400 rounded-lg my-4 ">
                        <div><i class="fa-solid fa-file"></i></div>
                        <div class="ml-4">${files[0].name}</div>
                    </div>`;
    
    filesList.appendChild(div);
});