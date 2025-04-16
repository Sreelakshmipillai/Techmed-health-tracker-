const wrapper= document.querySelector('.wrapper');
const loginLink= document.querySelector('.login-link');
const registerLink= document.querySelector('.register-link');
const btnPopup= document.querySelector('.btnLogin-popup');
const iconClose= document.querySelector('.icon-close');


registerLink.addEventListener('click',()=>{
    wrapper.classList.add('active');
    
});

loginLink.addEventListener('click',()=>{
    wrapper.classList.remove('active');
    
});

btnPopup.addEventListener('click',()=>{
    wrapper.classList.add('active-popup');
    
});
iconClose.addEventListener('click',()=>{
    wrapper.classList.remove('active-popup');
    
});


/// aski ai
const btnChatbotPopup = document.querySelector('.btnChatbot-popup');
const wrapperChatbot = document.querySelector('.wrapper1');
const iconCloseChatbot = document.querySelector('.chatbot-close'); // Correct close button selector

btnChatbotPopup.addEventListener('click', () => {
    wrapperChatbot.classList.add('active-popup');
});

iconCloseChatbot.addEventListener('click', () => {
    wrapperChatbot.classList.remove('active-popup');
});
