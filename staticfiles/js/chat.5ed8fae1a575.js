const API_KEY = "AIzaSyAOqXwmnbgtLgWMNZJlYFey7XD8F9t25WI"; // Your Gemini API Key

const SYSTEM_PROMPT = `You are Compliance AI, an expert assistant that specializes in helping organizations understand and implement compliance requirements across various industries and regulations.

**Core Mission:**
- Provide clear, actionable compliance guidance
- Help interpret complex regulations and standards
- Analyze documents for compliance requirements
- Extract and explain annexes, clauses, and specific requirements from documents
- Offer practical implementation strategies
- Ensure accuracy in regulatory information
- Support risk management and audit preparation

**Expertise Areas:**
- Data Privacy (GDPR, CCPA, HIPAA, etc.)
- Cybersecurity Compliance (SOX, PCI DSS, ISO 27001)
- Financial Regulations (SOX, Basel III, MiFID II)
- Industry Standards (FDA, OSHA, SEC)
- Corporate Governance and Risk Management
- Audit Preparation and Documentation
- Policy Development and Review
- Document Analysis and Interpretation

**Document Analysis Capabilities:**
- Extract all annexes, appendices, and schedules from compliance documents
- Identify and explain all clauses and sub-clauses
- Summarize key requirements and obligations
- Highlight critical deadlines and timelines
- Map document sections to compliance frameworks
- Provide implementation guidance for specific requirements

**Communication Style:**
- Professional and direct
- Clear explanations without unnecessary formatting
- Practical, implementable advice
- Step-by-step guidance for compliance processes
- Risk-aware recommendations
- Always include relevant disclaimers when appropriate
- Provide references to official sources when possible

**Response Format:**
- Start with relevant compliance context
- Provide clear, structured guidance
- Break down complex requirements into manageable steps
- Highlight key risks and considerations
- Reference relevant standards or regulations
- Offer practical implementation tips

**Important Notes:**
- Always recommend consulting with legal professionals for complex matters
- Stay current with regulatory changes and updates
- Emphasize the importance of regular compliance reviews
- When analyzing documents, be thorough and extract all relevant structural elements
- For document analysis requests, provide comprehensive breakdowns of annexes, clauses, and requirements

Remember: Accuracy is paramount in compliance matters. When analyzing documents, be systematic and thorough in identifying all structural elements and requirements.`;

let chatHistory = [
    { role: "user", parts: [{ text: SYSTEM_PROMPT }] },
    { role: "model", parts: [{ text: "Hello! I'm your Compliance AI assistant, ready to help you navigate regulatory requirements and analyze compliance documents. I can provide guidance on various regulations, analyze documents for specific requirements, extract annexes and clauses, and offer practical implementation advice. What can I help you with today?" }] }
];

// Document upload and processing functionality
let uploadedDocuments = [];

function handleFileUpload(event) {
    const files = Array.from(event.target.files);
    files.forEach(file => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const document = {
                name: file.name,
                content: e.target.result,
                type: file.type,
                uploadDate: new Date().toISOString()
            };
            uploadedDocuments.push(document);
            displayDocumentUploaded(file.name);
        };
        
        if (file.type.includes('text') || file.name.endsWith('.txt')) {
            reader.readAsText(file);
        } else {
            reader.readAsDataURL(file);
        }
    });
}

function displayDocumentUploaded(fileName) {
    displayMessage(`Document uploaded: ${fileName}. I can now analyze this document for compliance requirements, annexes, clauses, and provide detailed breakdowns. Ask me questions about its contents!`, 'bot');
}

function getDocumentContext() {
    if (uploadedDocuments.length === 0) return "";
    
    let context = "\n\nUploaded Documents Context:\n";
    uploadedDocuments.forEach((doc, index) => {
        context += `Document ${index + 1}: ${doc.name}\n`;
        if (doc.type.includes('text')) {
            context += `Content: ${doc.content.substring(0, 2000)}...\n\n`;
        }
    });
    return context;
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function displayMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    // Show chat messages container and hide title when first message appears
    if (!chatMessages.classList.contains('has-messages')) {
        chatMessages.classList.add('has-messages');
        const chatTitle = document.querySelector('.chat-title');
        if (chatTitle) {
            chatTitle.style.display = 'none';
        }
    }

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user' : 'assistant');
    
    const avatar = document.createElement('div');
    avatar.classList.add('message-avatar');
    
    const content = document.createElement('div');
    content.classList.add('message-content');
    
    // Format the message content properly
    let formattedMessage = message
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Handle bullet points and numbered lists
    formattedMessage = formattedMessage.replace(/^• (.+)$/gm, '<li>$1</li>');
    formattedMessage = formattedMessage.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
    if (formattedMessage.includes('<li>')) {
        formattedMessage = formattedMessage.replace(/(<li>.*?<\/li>)/gs, '<ul>$1</ul>');
    }
    
    content.innerHTML = formattedMessage;
    
    if (sender === 'user') {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
        messageDiv.appendChild(content);
        messageDiv.appendChild(avatar);
    } else {
        avatar.innerHTML = '<i class="fas fa-gavel"></i>';
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.classList.add('show');
        scrollToBottom();
    }
    
    // Show global loading overlay
    showGlobalLoader();
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.classList.remove('show');
    }
    
    // Hide global loading overlay
    hideGlobalLoader();
}

function showGlobalLoader() {
    let loader = document.getElementById('globalLoader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'globalLoader';
        loader.innerHTML = `
            <div class="global-loader-content">
                <div class="loader-spinner"></div>
                <div class="loader-text">AI is thinking...</div>
            </div>
        `;
        document.body.appendChild(loader);
    }
    loader.classList.add('show');
}

function hideGlobalLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) {
        loader.classList.remove('show');
    }
}

function toggleLoading(show) {
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.disabled = show;
        if (show) {
            // Show loading spinner
            sendButton.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" class="loading-spinner">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="31.416" stroke-dashoffset="31.416">
                        <animate attributeName="stroke-dasharray" dur="2s" values="0 31.416;15.708 15.708;0 31.416" repeatCount="indefinite"/>
                        <animate attributeName="stroke-dashoffset" dur="2s" values="0;-15.708;-31.416" repeatCount="indefinite"/>
                    </circle>
                </svg>
            `;
        } else {
            // Restore send icon
            sendButton.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
            `;
        }
    }
}

async function sendMessageToGemini(userMessage) {
    if (!userMessage.trim()) return;

    toggleLoading(true);
    showTypingIndicator();
    
    // Add document context to user message if documents are uploaded
    const messageWithContext = userMessage + getDocumentContext();
    
    chatHistory.push({ role: "user", parts: [{ text: messageWithContext }] });
    displayMessage(userMessage, 'user');

    const payload = { contents: chatHistory };
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`;

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("API Error:", errorData);
            throw new Error(`HTTP error! status: ${response.status} - ${errorData.error?.message || 'Unknown error'}`);
        }

        const result = await response.json();

        if (result.candidates && result.candidates.length > 0 &&
            result.candidates[0].content && result.candidates[0].content.parts &&
            result.candidates[0].content.parts.length > 0) {
            const botResponse = result.candidates[0].content.parts[0].text;
            chatHistory.push({ role: "model", parts: [{ text: botResponse }] });
            hideTypingIndicator();
            displayMessage(botResponse, 'bot');
        } else {
            hideTypingIndicator();
            displayMessage("I'm experiencing some technical difficulties right now. Please try rephrasing your compliance question, and I'll do my best to help you navigate the regulatory landscape.", 'bot');
            console.error("Unexpected API response structure:", result);
        }
    } catch (error) {
        console.error("Error communicating with Gemini API:", error);
        hideTypingIndicator();
        displayMessage("I'm currently experiencing connectivity issues. Please try again in a moment, or feel free to rephrase your compliance question in a different way.", 'bot');
    } finally {
        toggleLoading(false);
    }
}

function handleSendMessage() {
    const chatInput = document.getElementById('chatInput');
    if (!chatInput) return;
    
    const message = chatInput.value.trim();
    if (message) {
        sendMessageToGemini(message);
        chatInput.value = '';
        chatInput.style.height = 'auto';
    }
}

function clearDocuments() {
    uploadedDocuments = [];
    displayMessage("All uploaded documents have been cleared from memory.", 'bot');
}

// Inject CSS for loading animations
function injectLoaderCSS() {
    if (!document.querySelector('#chat-loader-styles')) {
        const loaderCSS = `
        .loading-spinner {
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .send-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .typing-indicator.show {
            display: block;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Global Loader Styles */
        #globalLoader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease-in-out;
        }

        #globalLoader.show {
            opacity: 1;
            visibility: visible;
        }

        .global-loader-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            text-align: center;
            min-width: 200px;
            animation: slideUp 0.4s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .loader-spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        .loader-text {
            color: #333;
            font-size: 16px;
            font-weight: 500;
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .global-loader-content {
                background: #2a2a2a;
                color: white;
            }
            
            .loader-text {
                color: #fff;
            }
            
            .loader-spinner {
                border-color: #444;
                border-top-color: #007bff;
            }
        }
        `;
        
        const style = document.createElement('style');
        style.id = 'chat-loader-styles';
        style.textContent = loaderCSS;
        document.head.appendChild(style);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Inject loader CSS
    injectLoaderCSS();
    
    const sendButton = document.getElementById('sendButton');
    const chatInput = document.getElementById('chatInput');
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');
    const clearDocsButton = document.getElementById('clearDocsButton');

    // Auto-resize textarea
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }

    // Send button click handler
    if (sendButton) {
        sendButton.addEventListener('click', handleSendMessage);
    }

    // File upload handlers
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }
    
    if (uploadButton) {
        uploadButton.addEventListener('click', () => {
            fileInput?.click();
        });
    }
    
    if (clearDocsButton) {
        clearDocsButton.addEventListener('click', clearDocuments);
    }

    // Enter key handler
    if (chatInput) {
        chatInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                handleSendMessage();
            }
        });
    }

    // Welcome message
    setTimeout(() => {
        displayMessage(`Welcome! I'm your Compliance AI assistant. I can help you with regulatory guidance, document analysis, and compliance implementation.

Key capabilities:
- Analyze compliance documents and extract all annexes, clauses, and requirements
- Provide guidance on GDPR, HIPAA, SOX, ISO 27001, and other regulations
- Help with policy development and audit preparation
- Answer questions about specific compliance requirements

You can upload documents for analysis or ask me any compliance-related questions. What would you like to help with today?`, 'bot');
    }, 1000);
});