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

//SUBIDO MEDIANTE UN DROP!
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    fileInput.files = files;  // Asignar los archivos al input de tipo file
    console.log("Archivo cargado en el formulario:", fileInput.files[0]);  // Opcional: ver el archivo en la consola


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

// SUBIDO MANUALMNTE
fileInput.addEventListener('change', function() {
    const files = fileInput.files;

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
});