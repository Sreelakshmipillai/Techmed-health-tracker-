// Authentication popups
const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
});

// Chatbot popup
const btnChatbotPopup = document.querySelector('.btnChatbot-popup');
const wrapperChatbot = document.querySelector('.wrapper1');
const iconCloseChatbot = document.querySelector('.chatbot-close');

btnChatbotPopup.addEventListener('click', () => {
    wrapperChatbot.classList.add('active-popup');
});

iconCloseChatbot.addEventListener('click', () => {
    wrapperChatbot.classList.remove('active-popup');
});

// Chatbot Interaction
const sendButton = document.querySelector('.send-btn');
const inputField = document.querySelector('.wrapper1 .input-box input');
const chatBox = document.getElementById('chatbox');

// Function to send user message to server
async function sendMessage(userMessage) {
    try {
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        });
        const data = await response.json();
        return data.reply;
    } catch (error) {
        console.error('Error communicating with server:', error);
        return "Sorry, the server seems to be down. Please try again later.";
    }
}

// Function to handle sending and displaying messages
async function handleSendMessage() {
    const userMessage = inputField.value.trim();
    if (userMessage !== '') {
        // Display user message
        const userMsgElem = document.createElement('p');
        userMsgElem.innerHTML = `<strong>You:</strong> ${userMessage}`;
        chatBox.appendChild(userMsgElem);

        // Display typing animation
        const typingElem = document.createElement('p');
        typingElem.setAttribute('id', 'typing');
        typingElem.innerHTML = `<strong>Bot:</strong> typing...`;
        chatBox.appendChild(typingElem);

        chatBox.scrollTop = chatBox.scrollHeight;

        // Fetch bot reply
        const botReply = await sendMessage(userMessage);

        // Replace typing... with actual reply
        typingElem.innerHTML = `<strong>Bot:</strong> ${botReply}`;

        // Clear input field
        inputField.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Button click event
sendButton.addEventListener('click', handleSendMessage);

// Enter key event
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendButton.click();
    }
});
