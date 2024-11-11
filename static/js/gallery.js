function openImageFullscreen(imgElement) {
        const imageUrl = imgElement.src; // Получаем URL изображения
        const imageAlt = imgElement.alt; // Получаем альтернативный текст

        // Отправляем данные в родительское окно
        window.parent.postMessage({ imageUrl: imageUrl, imageAlt: imageAlt }, '*');
    }

    // Функция для отправки высоты контента родителю
function sendHeightToParent() {
    const height = document.body.scrollHeight + 30; // Получаем высоту всего контента
    window.parent.postMessage(height, '*'); // Отправляем высоту родителю
}

    // Отправляем высоту после загрузки страницы
    window.addEventListener('load', sendHeightToParent);

    // Отправляем высоту при изменении размеров окна, если контент изменяется динамически
    window.addEventListener('resize', sendHeightToParent);

    // Определяем функцию toggleNavigation для переключения состояния навигации
function toggleNavigation() {
    const navFrame = document.getElementById('sidebar');
    const galleryFrame = document.querySelector('.gallery-frame');

    if (navFrame && galleryFrame) {
        if (navFrame.style.display === 'none' || navFrame.style.display === '') {
            navFrame.style.display = 'block';
            galleryFrame.style.width = '75%';
            window.frames['galleryFrame'].postMessage('navOpened', '*'); // Отправить сообщение о том, что навигация открыта
        } else {
            navFrame.style.display = 'none';
            galleryFrame.style.width = '100%';
            window.frames['galleryFrame'].postMessage('navClosed', '*'); // Отправить сообщение о том, что навигация закрыта
        }
    } else {
        console.error("Не удалось найти элементы с ID 'sidebar' или 'gallery-frame'");
    }
}

    // Обработчик сообщений из фрейма с галереей
window.addEventListener('message', function(event) {
    if (event.data === 'toggleNavigation') {
        toggleNavigation(); // Вызов функции переключения навигации
    }
});


    window.addEventListener('message', function(event) {
        // Проверяем, что полученное значение — это высота
        const newHeight = parseInt(event.data);
        const navFrame = document.getElementById('sidebar');

        if (!isNaN(newHeight)) {
            // Применяем полученную высоту к фрейму галереи
            const galleryFrame = document.querySelector('.gallery-frame');
            galleryFrame.style.height = `${newHeight}px`; // Устанавливаем высоту фрейма
            navFrame.style.height = `${newHeight}px`;
        }
    });

    // Открытие модального окна с получением данных через postMessage
    function openModal(imageUrl, imageAlt) {
        const modal = document.getElementById("modal");
        const modalImg = document.getElementById("modal-img");
        const captionText = document.getElementById("caption");

        modal.style.display = "block";
        modalImg.src = imageUrl;
        captionText.innerHTML = imageAlt;
    }

    // Закрытие модального окна
    function closeModal() {
        const modal = document.getElementById("modal");
        modal.style.display = "none";
    }

    // Получаем сообщение от фрейма и открываем модальное окно
    window.addEventListener('message', function(event) {
        if (event.data && event.data.imageUrl) {
            openModal(event.data.imageUrl, event.data.imageAlt);
        }
    });