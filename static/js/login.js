// Переключение между формой входа и регистрации
document.getElementById('show-register').onclick = function() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('register-container').style.display = 'block';
};

document.getElementById('show-login').onclick = function() {
    document.getElementById('register-container').style.display = 'none';
    document.getElementById('login-container').style.display = 'block';
};

// Функция для корректного формата поля с телефоном
function formatPhoneInput(input) {
    const cursorPosition = input.selectionStart;
    if (!input.value.startsWith('+7')) {
        input.value = '+7';
    }
    if (cursorPosition <= 2) {
        input.setSelectionRange(3, 3);
    }
}

// Обработка ввода в поле телефона
document.getElementById('login-phone').addEventListener('input', function() {
    formatPhoneInput(this);
});

document.getElementById('register-phone').addEventListener('input', function() {
    formatPhoneInput(this);
});