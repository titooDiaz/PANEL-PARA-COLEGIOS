const input_file = document.getElementById('file_input');
const modal = document.getElementById('file_modal');
const preview = document.getElementById('file_preview');
const cancel = document.getElementById('cancel_file');
const accept = document.getElementById('accept_file');
const fileNameText = document.getElementById('file_name');

let tempFile = null;

input_file.addEventListener('change', function () {

    if (!this.files[0]) return;
    tempFile = this.files[0];
    preview.innerHTML = '';

    const fileType = tempFile.type;

    if (fileType.startsWith('image/')) {
    const img = document.createElement('img');
    const url = URL.createObjectURL(tempFile);
    img.src = url;
    tempFile.previewURL = url;
    img.className = 'max-w-full max-h-60 rounded';
    preview.appendChild(img);
    } else if (fileType === 'application/pdf') {
    const url = URL.createObjectURL(tempFile);
    tempFile.previewURL = url;
    preview.innerHTML = `<embed src="${url}" type="application/pdf" width="100%" height="100%" />`;
    } else {
    preview.innerHTML = `<p class="text-sm text-gray-600">Archivo seleccionado: <strong>${tempFile.name}</strong></p>`;
    }

    modal.classList.remove('hidden');
});

cancel.addEventListener('click', () => {
    // Limpiar input_file
    input_file.value = '';

    // Limpiar preview
    preview.innerHTML = '';

    // Quitar nombre visible
    if (fileNameText) {
    fileNameText.textContent = '';
    }

    // Ocultar modal
    modal.classList.add('hidden');

    // Liberar memoria
    if (tempFile && tempFile.previewURL) {
    URL.revokeObjectURL(tempFile.previewURL);
    }

    tempFile = null;
});

accept.addEventListener('click', () => {
    if (tempFile) {
    fileNameText.textContent = tempFile.name;
    }

    // Ocultar modal
    modal.classList.add('hidden');
});

const toggleContactsBtn = document.getElementById('toggleContacts');
const contacts = document.getElementById('contacts');
toggleContactsBtn?.addEventListener('click', () => {
    contacts.classList.toggle('visible');
});

const scrollContainer = document.getElementById('messages-container');

function scrollToBottom() {
    scrollContainer.scrollTo({ top: scrollContainer.scrollHeight, behavior: 'smooth' });
}

window.addEventListener('load', scrollToBottom);

const user1Id = document.getElementById('user1Id').textContent.trim();
const user2Id = document.getElementById('user2Id').textContent.trim();
const sender = document.getElementById('sender').textContent.trim();
const receiver = document.getElementById('receiver').textContent.trim();

const csrfToken = document.getElementById('secret_token').textContent.trim();
const url_chat_file = document.getElementById('url_chat_file').textContent;
const photo_url = document.getElementById('photo_url').textContent;
const protocol1 = window.location.protocol === "https:" ? "wss" : "ws";
const chatSocket = new WebSocket(
    `${protocol1}://${window.location.host}/ws/chat/${user1Id}_${user2Id}/`
);

const container = document.getElementById('chat-box');
const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("message_input");

sendBtn.addEventListener("click", async function () {
    const message = input.value.trim();
    const file = input_file.files[0];

    if (!message && !file) return;

    let fileData = null;

    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('csrfmiddlewaretoken', csrfToken);

        try {
            const response = await fetch(url_chat_file, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error("Error al subir archivo");

            fileData = await response.json();  // { url, name, type }
        } catch (error) {
            alert("Error subiendo archivo: " + error.message);
            return;
        }
    }

    chatSocket.send(JSON.stringify({
        type: "chat",
        message: message,
        sender_id: sender,
        receiver_id: receiver,
        file: fileData
    }));

    input.value = '';
    input_file.value = '';
    fileNameText.textContent = '';
});

input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendBtn.click();
    }
});

// user in chat?
const statusIndicator = document.getElementById("status_indicator");

let typingTimeout = null;

// Listen to WebSocket messages
// Listen to all socket messages
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type === "chat") {
        // handle message normally
        const div = document.createElement('div');
        div.className = data.sender_id == sender
            ? 'flex items-end justify-end space-x-2'
            : 'flex items-start space-x-2';

        let fileHtml = '';
        if (data.file) {
            const fileUrl = data.file.url;
            const fileType = data.file.type;
            fileHtml = `<a href="${fileUrl}" target="_blank" class="block mt-2 text-blue-500 underline">📎 Ver archivo</a>`;
        }

        div.innerHTML = `
            ${data.sender_id !== sender ? `<img src="${photo_url}" alt="Foto" class="w-8 h-8 rounded-full">` : ''}
            <div class="${data.sender_id === sender ? 'bg-gray-600 text-white' : 'bg-white'} rounded-lg p-3 shadow-md max-w-md">
                <p>${data.message}</p>
                ${fileHtml}
            </div>
            <span class="text-gray-500 text-xs message-time">
                ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </span>
        `;
        container.appendChild(div);
        scrollToBottom();
    }

    if (data.type === "status") {
        statusIndicator.textContent = data.status === "online" ? "🟢 Online" : "⚪ Offline";
    }

    if (data.type === "typing") {
        if (data.user_id != sender) {
            const styleExists = document.getElementById('typing-style');
            // Solo crear si aún no existe
            if (!document.getElementById('typing-bubbles')) {
                const div = document.createElement('div');
                div.id = 'typing-bubbles';
                div.className = 'flex items-start space-x-2';
                div.innerHTML = `
                    <img src="${photo_url}" alt="Foto" class="w-8 h-8 rounded-full">
                    <div class="bg-white rounded-lg p-3 shadow-md max-w-md">
                        <div class="flex space-x-1 items-end mt-1">
                            <div class="w-2 h-2 bg-orange-600 rounded-full typing-dot"></div>
                            <div class="w-2 h-2 bg-orange-600 rounded-full typing-dot"></div>
                            <div class="w-2 h-2 bg-orange-600 rounded-full typing-dot"></div>
                        </div>
                    </div>
                `;
                container.appendChild(div);
                scrollToBottom();
            }
        }
    }

    if (data.type === "stop_typing") {
        if (data.user_id != sender) {
            const typingDiv = document.getElementById('typing-bubbles');
            if (typingDiv) {
                typingDiv.remove();
            }
        }
    }
};


// Emit typing events
input.addEventListener("input", () => {
  chatSocket.send(JSON.stringify({
    type: "typing",
    sender_id: sender
  }));

  clearTimeout(typingTimeout);
  typingTimeout = setTimeout(() => {
    chatSocket.send(JSON.stringify({
      type: "stop_typing",
      sender_id: sender
    }));
  }, 1000); // stop typing after 1s of inactivity
});
