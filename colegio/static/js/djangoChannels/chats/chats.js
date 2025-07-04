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
        sender_id: sender,
        receiver_id: receiver,
        message: message,
        file: fileData,
        reply_to: replyingToId || null
    }));

    cancelReply();
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

let loadingOldMessages = false;
let hasMorePages = true;
let lastScrollTop = 0;

function scrollHandler() {
    const goingUp = scrollContainer.scrollTop < lastScrollTop;
    const nearTop = scrollContainer.scrollTop <= 50;

    if (goingUp && nearTop && !loadingOldMessages && hasMorePages) {
        loadingOldMessages = true;

        const oldestMessage = container.querySelector('[data-msg-id]');
        const lastMessageId = oldestMessage?.dataset?.msgId || null;

        chatSocket.send(JSON.stringify({
            type: "load_more",
            before_id: lastMessageId,
            sender_id: sender,
            receiver_id: receiver
        }));
    }

    lastScrollTop = scrollContainer.scrollTop;
}

scrollContainer.addEventListener('scroll', scrollHandler);

// Listen to WebSocket messages
// Listen to all socket messages
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type === "chat") {
        renderMessage(data, data.sender_id == sender, false);
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
                    <div class="bg-white rounded-lg p-3 shadow-md max-w-md">
                        <div class="flex space-x-1 items-end">
                            <div class="typing-dot w-3 h-3 bg-orange-600 rounded-full"></div>
                            <div class="typing-dot w-3 h-3 bg-orange-600 rounded-full"></div>
                            <div class="typing-dot w-3 h-3 bg-orange-600 rounded-full"></div>
                        </div>
                `;
                container.appendChild(div);
                scrollToBottom();
            }
        }
    }

    if (data.type === "more") {
        const scrollBefore = scrollContainer.scrollHeight;

        data.messages.forEach(msg => {
            renderMessage(msg, msg.sender_id == sender, true);
        });

        const scrollAfter = scrollContainer.scrollHeight;
        scrollContainer.scrollTop = scrollAfter - scrollBefore;

        if (!data.has_next) {
            hasMorePages = false;
        }

        loadingOldMessages = false;
    }



    if (data.type === "deleted") {
        const messageDiv = document.querySelector(`[data-msg-id="${data.id}"]`);
        if (messageDiv) {
            const messageContent = messageDiv.querySelector('.message-content');
            if (messageContent) {
                messageContent.innerHTML = `<p class="italic text-gray-400">🗑️ Este mensaje fue eliminado</p>`;
            }

            const buttons = messageDiv.querySelector('.action-buttons');
            if (buttons) {
                buttons.remove();
            }
        }
    }

    if (data.type === "highlight") {
        const messageDiv = document.querySelector(`[data-msg-id="${data.id}"]`);
        if (messageDiv) {
            const messageContent = messageDiv.querySelector('.message-content');
            if (messageContent) {
                messageContent.classList.toggle('glow-important');
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

function renderMessage(msg, isSender, prepend = false) {
    const div = document.createElement('div');
    div.dataset.msgId = msg.id;

    // Determine wrapper class based on sender
    div.className = `message-wrapper relative ${isSender ? 'flex items-end justify-end space-x-2' : 'flex items-start space-x-2'}`;

    // If there's a file attached
    const fileHtml = msg.file
        ? `<a href="${msg.file.url}" target="_blank" class="block mt-2 text-blue-500 underline text-sm">📎 View file</a>`
        : '';

    const isImportant = msg.important && !msg.deleted;

    // Base content class
    const contentClass = [
        "message-content",
        "rounded-lg",
        "p-3",
        "shadow-md",
        "max-w-md",
        isSender ? "bg-gray-600 text-white" : "bg-white",
    ];

    // Add glow effect if message is marked as important
    if (isImportant) {
        contentClass.push("glow-important");
    }

    // Action buttons for each side
    const actionButtons = isSender
        ? `
        <div class="action-buttons absolute top-1 right-1 bg-white shadow-md rounded-lg px-2 py-1 flex space-x-1 z-50">
            <button class="text-sm text-red-600 hover:bg-red-100 p-1 rounded-full" onclick="deleteMessage('${msg.id}')">🗑️</button>
            <button class="text-sm text-yellow-600 hover:bg-yellow-100 p-1 rounded-full" onclick="replyToMessage('${msg.id}')">↩️</button>
            <button class="text-sm text-green-600 hover:bg-green-100 p-1 rounded-full" onclick="highlightMessage('${msg.id}')">⭐</button>
        </div>`
        : `
        <div class="action-buttons absolute top-1 left-1 bg-white shadow-md rounded-lg px-2 py-1 flex space-x-1 z-50">
            <button class="text-sm text-yellow-600 hover:bg-yellow-100 p-1 rounded-full" onclick="replyToMessage('${msg.id}')">↩️</button>
            <button class="text-sm text-green-600 hover:bg-green-100 p-1 rounded-full" onclick="highlightMessage('${msg.id}')">⭐</button>
        </div>`;

    // Final message HTML structure
    div.innerHTML = `
        <div class="${contentClass.join(' ')}">
            <div class="no-select-overlay"></div>

            ${msg.reply ? `
                <div class="mb-2 border-l-4 pl-2 border-gray-400 text-sm text-gray-500 italic max-w-[80%] line-clamp-1">
                    <span class="ml-2">${msg.reply}</span>
                </div>` : ''}

            <p class="break-words">
                ${msg.deleted ? '<span class="italic text-gray-400">🗑️ This message was deleted</span>' : msg.message}
            </p>

            ${!msg.deleted && fileHtml ? fileHtml : ''}
        </div>

        ${!msg.deleted ? actionButtons : ''}

        <span class="block text-right text-xs text-gray-400 mt-1 mr-2">
            ${msg.timestamp ?? new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
    `;

    // Add interactions for showing action buttons
    const wrapper = div;
    const buttons = wrapper.querySelector('.action-buttons');

    let timeout = null;
    div.addEventListener('click', () => toggleButtons(buttons, wrapper));
    div.addEventListener('touchstart', () => {
        timeout = setTimeout(() => toggleButtons(buttons, wrapper), 500);
    });
    div.addEventListener('touchend', () => clearTimeout(timeout));
    div.addEventListener('touchmove', () => clearTimeout(timeout));

    // Append or prepend the message to the container
    if (prepend) {
        container.prepend(div);
    } else {
        container.appendChild(div);
        scrollToBottom();
    }
}


function deleteMessage(messageId) {
    const confirmed = window.confirm("¿Estás seguro de que quieres eliminar este mensaje?");

    if (!confirmed) return;

    chatSocket.send(JSON.stringify({
        type: "delete",
        message_id: messageId
    }));

    const messageDiv = document.querySelector(`[data-msg-id="${messageId}"]`);
    if (messageDiv) {
        const messageContent = messageDiv.querySelector('.message-content');
        if (messageContent) {
            messageContent.innerHTML = `<p class="italic text-gray-400">🗑️ Este mensaje fue eliminado</p>`;
        }

        const buttons = messageDiv.querySelector('.action-buttons');
        if (buttons) {
            buttons.remove();
        }
    }
}

function highlightMessage(messageId) {
    chatSocket.send(JSON.stringify({
        type: "highlight",
        message_id: messageId
    }));
}


let replyingToId = null;

function replyToMessage(messageId) {
    const msgDiv = document.querySelector(`[data-msg-id="${messageId}"]`);
    if (!msgDiv) return;

    const textElement = msgDiv.querySelector('.message-content p');
    const text = textElement ? textElement.textContent : 'mensaje';

    // Mostramos el contenedor con el texto
    document.getElementById('reply-box').classList.remove('hidden');
    document.getElementById('reply-text').textContent = text.length > 100 ? text.slice(0, 100) + '…' : text;
    
    replyingToId = messageId;
}

function cancelReply() {
    replyingToId = null;
    document.getElementById('reply-box').classList.add('hidden');
    document.getElementById('reply-text').textContent = '';
}


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
