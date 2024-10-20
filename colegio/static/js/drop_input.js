const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('archivo');
const filesList = document.getElementById('files_list'); // Lista de archivos subidos
let storedFiles = [];  // Aquí acumulamos todos los archivos seleccionados

// Prevenir comportamientos por defecto para eventos de arrastrar y soltar
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Manejar el evento "drop"
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const newFiles = Array.from(dt.files);  // Convertir a array
    addFilesToList(newFiles);
    displayFiles(newFiles);
}

// SUBIDA MANUAL
fileInput.addEventListener('change', function() {
    const newFiles = Array.from(fileInput.files);  // Convertir a array
    addFilesToList(newFiles);
    displayFiles(newFiles);
});

function addFilesToList(newFiles) {
    // Agregar los nuevos archivos a la lista global almacenada
    storedFiles = [...storedFiles, ...newFiles];
}

function displayFiles(files) {
    // Recorrer todos los archivos seleccionados
    files.forEach(file => {
        // Crear un elemento HTML e insertarlo en el DOM para cada archivo
        const div = document.createElement('div');
        div.innerHTML = `
            <div class="p-4 flex w-full bg-green-400 rounded-lg my-4 ">
                <div><i class="fa-solid fa-file"></i></div>
                <div class="ml-4">${file.name}</div>
            </div>
        `;
        filesList.appendChild(div);
    });
}

// Función para actualizar el input con los archivos antes de enviar el formulario
function updateFileInputBeforeSubmit() {
    const dataTransfer = new DataTransfer();
    storedFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
}

// Agregar un evento al formulario para asegurarse de que los archivos se pasen al input antes de enviar
document.querySelector('form').addEventListener('submit', function(e) {
    updateFileInputBeforeSubmit();
});
