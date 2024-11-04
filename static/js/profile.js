// Получение элементов
        const editButton = document.getElementById('edit-button');
        const cancelButton = document.getElementById('cancel-button');
        const userInfo = document.getElementById('user-info');
        const editForm = document.getElementById('edit-form');
        const profileForm = document.getElementById('profile-form');
        const avatarForm = document.getElementById('avatar-block');

        // Обработчик нажатия на кнопку "Редактировать данные"
        editButton.addEventListener('click', () => {
            userInfo.style.display = 'none';
            editForm.style.display = 'block';
            avatarForm.style.display = 'none';
        });

        // Обработчик нажатия на кнопку "Отмена"
    cancelButton.addEventListener('click', () => {
        editForm.style.display = 'none';
        userInfo.style.display = 'block';
        avatarForm.style.display = 'block';
        clearMessages(); // Очищаем сообщения о статусе
        profileForm.reset(); // Сбрасываем форму
    });

    // Функция для очистки сообщений о статусе
    function clearMessages() {
        const messages = document.querySelectorAll('.messages');
        messages.forEach(messageList => {
            messageList.innerHTML = ''; // Очищаем содержимое списка сообщений
        });
    }