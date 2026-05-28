document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const typingIndicator = document.getElementById('typing-indicator');
    const audioPlayer = document.getElementById('audio-player');
    const logo = document.querySelector('.logo');

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isRecording = false;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        
        recognition.onstart = () => {
            isRecording = true;
            micBtn.classList.add('recording');
            messageInput.placeholder = "Listening...";
        };
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            messageInput.value = transcript;
            sendMessage();
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            stopRecording();
        };
        
        recognition.onend = () => {
            stopRecording();
        };
    } else {
        micBtn.style.display = 'none';
        console.warn("Speech Recognition not supported in this browser.");
    }

    function stopRecording() {
        isRecording = false;
        micBtn.classList.remove('recording');
        messageInput.placeholder = "Type or speak your message...";
    }

    micBtn.addEventListener('click', () => {
        if (!recognition) return;
        
        if (isRecording) {
            recognition.stop();
        } else {
            // Stop any playing audio before recording
            audioPlayer.pause();
            audioPlayer.currentTime = 0;
            logo.classList.remove('speaking');
            
            recognition.start();
        }
    });

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value === '') {
            this.style.height = 'auto';
        }
    });

    // Handle enter key to send
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        // Add user message to UI
        appendMessage('user', text);
        messageInput.value = '';
        messageInput.style.height = 'auto';
        
        // Show typing indicator
        typingIndicator.classList.remove('hidden');
        scrollToBottom();

        try {
            // Send to DeepSeek backend
            const chatRes = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            
            const chatData = await chatRes.json();
            
            if (chatData.error) throw new Error(chatData.error);
            
            const aiText = chatData.response;
            
            // Hide typing indicator and show AI message
            typingIndicator.classList.add('hidden');
            appendMessage('assistant', aiText);
            
            // Request TTS for the response
            logo.classList.add('speaking');
            
            const ttsRes = await fetch('/api/tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: aiText })
            });
            
            if (!ttsRes.ok) throw new Error("Failed to get audio");
            
            const audioBlob = await ttsRes.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            
            // Play the audio
            audioPlayer.src = audioUrl;
            await audioPlayer.play();
            
        } catch (error) {
            console.error(error);
            typingIndicator.classList.add('hidden');
            appendMessage('assistant', 'Sorry, an error occurred. Please check your API keys or connection.');
        }
    }

    // Handle audio ending
    audioPlayer.addEventListener('ended', () => {
        logo.classList.remove('speaking');
        // Automatically start listening again for continuous conversation
        if (recognition && !isRecording) {
            recognition.start();
        }
    });

    function appendMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        
        const iconClass = role === 'user' ? 'fa-user' : 'fa-robot';
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid ${iconClass}"></i></div>
            <div class="content">${escapeHTML(text)}</div>
        `;
        
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
});
