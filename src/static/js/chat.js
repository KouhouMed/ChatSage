document.addEventListener('DOMContentLoaded', (event) => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const modelSelect = document.getElementById('modelSelect');
    const clearHistoryBtn = document.getElementById('clearHistory');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        const selectedModel = modelSelect.value;

        if (message) {
            addMessageToChat('You', message);
            userInput.value = '';

            try {
                const response = await axios.post('/api/chat', {
                    message: message,
                    model: selectedModel
                });

                addMessageToChat('ChatSage', response.data.response);
            } catch (error) {
                console.error('Error:', error);
                addMessageToChat('ChatSage', 'Sorry, an error occurred. Please try again.');
            }
        }
    });

    clearHistoryBtn.addEventListener('click', async () => {
        try {
            await axios.post('/api/clear_history');
            chatContainer.innerHTML = '';
            addMessageToChat('System', 'Chat history cleared.');
        } catch (error) {
            console.error('Error clearing history:', error);
            addMessageToChat('System', 'Error clearing chat history.');
        }
    });

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.className = `mb-2 ${sender === 'You' ? 'text-right' : 'text-left'}`;

        const textElement = document.createElement('span');
        textElement.className = `inline-block p-2 rounded-lg ${sender === 'You' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`;
        textElement.textContent = `${sender}: ${message}`;

        messageElement.appendChild(textElement);
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Load chat history when the page loads
    async function loadChatHistory() {
        try {
            const response = await axios.get('/api/history');
            response.data.history.forEach(message => {
                const [sender, content] = message.split(': ');
                addMessageToChat(sender, content);
            });
        } catch (error) {
            console.error('Error loading chat history:', error);
            addMessageToChat('System', 'Error loading chat history.');
        }
    }

    loadChatHistory();
});