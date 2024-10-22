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

// Manejar el evento "drop"
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const newFiles = dt.files;
    addFilesToInput(newFiles);
    displayFiles(newFiles);
}

// SUBIDO MANUALMNTE
fileInput.addEventListener('change', function() {
    const newFiles = fileInput.files;
    displayFiles(newFiles);
});

function addFilesToInput(newFiles) {
    const dataTransfer = new DataTransfer();
    
    // Agregar los archivos anteriores que ya estaban en el input
    for (let i = 0; i < fileInput.files.length; i++) {
        dataTransfer.items.add(fileInput.files[i]);
    }

    // Agregar los nuevos archivos
    for (let i = 0; i < newFiles.length; i++) {
        dataTransfer.items.add(newFiles[i]);
    }

    // Actualizar los archivos en el input
    fileInput.files = dataTransfer.files;
}

function displayFiles(files) {
    // Recorrer todos los archivos seleccionados
    for (let i = 0; i < files.length; i++) {
        // Crear un elemento HTML e insertarlo en el DOM para cada archivo
        const div = document.createElement('div');
        div.innerHTML = `
                        <div class="p-4 flex w-full bg-green-400 rounded-lg my-4 ">
                            <div><i class="fa-solid fa-file"></i></div>
                            <div class="ml-4">${files[i].name}</div>
                        </div>
                        `;
        
        filesList.appendChild(div);
    }
}