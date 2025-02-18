function showMessage(message) {

    // How do you use this?
    //    <button onclick="showMessage('¡Mensaje emergente!')" class="px-4 py-2 bg-blue-500 text-white rounded">Mostrar mensaje</button>
    //    <div id="message-container"></div>
    //
    //<!--notices-->
    // <script src="{% static 'js/windows/modal_for.js' %}"></script>
    // <script src="{% static 'css/animations/notice.css' %}"></script> 

    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message');
  
    // Crear el botón de cierre
    const closeButton = document.createElement('button');
    closeButton.textContent = 'X';
    closeButton.classList.add('close-btn');
    closeButton.onclick = function() {
      messageContainer.remove();
    };
  
    // Añadir el mensaje y el botón de cierre al contenedor
    messageContainer.textContent = message;
    messageContainer.appendChild(closeButton);
  
    // Mostrar el mensaje en la pantalla
    document.getElementById('message-container').appendChild(messageContainer);
  
    // Mostrar el mensaje (esto es útil si se quiere animar)
    setTimeout(() => {
      messageContainer.style.display = 'block';
    }, 100);
  
    // Cerrar automáticamente el mensaje después de 4 segundos
    setTimeout(() => {
      messageContainer.remove();
    }, 4000);
  }