// Get references to the chatbot logo and window
const chatbotLogo = document.getElementById('chatbot-logo');
const chatbotWindow = document.getElementById('chatbot-window');

// Function to toggle the visibility of the chatbot window
function toggleChatbotWindow() {
  if (chatbotWindow.style.display === 'block') {
    chatbotWindow.style.display = 'none';
  } else {
    chatbotWindow.style.display = 'block';
  }
}

// Event listener to toggle chatbot window when clicking the logo
chatbotLogo.addEventListener('click', toggleChatbotWindow);

// Event listener to close chatbot window when clicking anywhere outside of it
document.addEventListener('click', function(event) {
  if (!chatbotLogo.contains(event.target) && !chatbotWindow.contains(event.target)) {
    chatbotWindow.style.display = 'none';
  }
});
