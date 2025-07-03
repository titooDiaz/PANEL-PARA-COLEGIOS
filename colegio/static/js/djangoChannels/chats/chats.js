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
        const div = document.createElement('div');

        // 🆔 Assign message ID for interaction detection
        div.dataset.msgId = data.id;

        const isSender = data.sender_id == sender;

        // 📎 Add file link if there's a file
        let fileHtml = '';
        if (data.file) {
            const fileUrl = data.file.url;
            fileHtml = `<a href="${fileUrl}" target="_blank" class="block mt-2 text-blue-500 underline text-sm">📎 View file</a>`;
        }

        // 🛠️ Define action buttons depending on the sender
        const actionButtons = isSender
            ? `
            <div class="action-buttons absolute top-1 right-1 bg-white shadow-md rounded-lg px-2 py-1 flex space-x-1 z-50">
                <button class="text-sm text-red-600 hover:bg-red-100 p-1 rounded-full" onclick="deleteMessage('${data.id}')">🗑️</button>
                <button class="text-sm text-yellow-600 hover:bg-yellow-100 p-1 rounded-full" onclick="replyToMessage('${data.id}')">↩️</button>
                <button class="text-sm text-green-600 hover:bg-green-100 p-1 rounded-full" onclick="highlightMessage('${data.id}')">⭐</button>
            </div>`
            : `
            <div class="action-buttons absolute top-1 left-1 bg-white shadow-md rounded-lg px-2 py-1 flex space-x-1 z-50">
                <button class="text-sm text-yellow-600 hover:bg-yellow-100 p-1 rounded-full" onclick="replyToMessage('${data.id}')">↩️</button>
                <button class="text-sm text-green-600 hover:bg-green-100 p-1 rounded-full" onclick="highlightMessage('${data.id}')">⭐</button>
            </div>`;

        // 💬 Construct the message wrapper
        div.className = `message-wrapper relative ${isSender ? 'flex items-end justify-end space-x-2' : 'flex items-start space-x-2'}`;

        div.innerHTML = `
            <div class="${isSender ? 'bg-gray-600 text-white' : 'bg-white'} message-content rounded-lg p-3 shadow-md max-w-md">
                <div class="no-select-overlay"></div>
                <p class="break-words">${data.message}</p>
                ${fileHtml}
            </div>
            ${actionButtons}
            <span class="block text-right text-xs text-gray-400 mt-1 mr-2">
                ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </span>
        `;

        // ⬇️ Append the new message to the chat container
        container.appendChild(div);
        scrollToBottom();

        // 🧠 Apply interaction logic to this new message only
        const wrapper = div.closest('.message-wrapper') || div;
        const buttons = wrapper.querySelector('.action-buttons');

        let timeout = null;

        // 🖱️ Click (desktop)
        div.addEventListener('click', () => toggleButtons(buttons, wrapper));

        // 📱 Long press (mobile)
        div.addEventListener('touchstart', () => {
            timeout = setTimeout(() => toggleButtons(buttons, wrapper), 500);
        });
        div.addEventListener('touchend', () => clearTimeout(timeout));
        div.addEventListener('touchmove', () => clearTimeout(timeout));
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
        // 📏 Store current scroll height before adding old messages
        const scrollBefore = scrollContainer.scrollHeight;

        data.messages.forEach(msg => {
            const div = document.createElement('div');

            // 🆔 Assign message ID for click detection
            div.dataset.msgId = msg.id;

            const isSender = msg.sender_id == sender;

            // 🎯 Apply layout depending on sender
            div.className = `message-wrapper relative ${isSender ? 'flex items-end justify-end space-x-2' : 'flex items-start space-x-2'}`;

            // 📎 Generate file link if there's a file
            let fileHtml = '';
            if (msg.file) {
                const fileUrl = msg.file.url;
                fileHtml = `<a href="${fileUrl}" target="_blank" class="block mt-2 text-blue-500 underline text-sm">📎 View file</a>`;
            }

            // 🛠️ Add action buttons (depends on sender)
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

            // 💬 Build message content
            div.innerHTML = `
                <div class="${isSender ? 'bg-gray-600 text-white' : 'bg-white'} message-content rounded-lg p-3 shadow-md max-w-md">
                    <div class="no-select-overlay"></div>
                    <p class="break-words">${msg.message}</p>
                    ${fileHtml}
                </div>
                ${actionButtons}
                <span class="block text-right text-xs text-gray-400 mt-1 mr-2">
                    ${msg.timestamp}
                </span>
            `;

            // ⬆️ Prepend old message to the container
            container.prepend(div);

            // 🧠 Apply interaction logic (click + long press)
            let timeout = null;
            const wrapper = div;
            const buttons = wrapper.querySelector('.action-buttons');

            div.addEventListener('click', () => toggleButtons(buttons, wrapper));
            div.addEventListener('touchstart', () => {
                timeout = setTimeout(() => toggleButtons(buttons, wrapper), 500);
            });
            div.addEventListener('touchend', () => clearTimeout(timeout));
            div.addEventListener('touchmove', () => clearTimeout(timeout));
        });

        // 🧮 Restore scroll position to avoid jumping
        const scrollAfter = scrollContainer.scrollHeight;
        scrollContainer.scrollTop = scrollAfter - scrollBefore;

        // 🚫 If there's no more data, stop loading
        if (!data.has_next) {
            hasMorePages = false;
        }

        loadingOldMessages = false;
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
