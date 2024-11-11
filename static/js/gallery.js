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

    function toggleNavigation() {
        const navFrame = document.getElementById('sidebar');
        const galleryFrame = document.getElementById('gallery-frame');
        const button = document.getElementById('open-nav-container')

        // Переключаем видимость навигации и галереи на весь экран
        if (navFrame.style.display === 'none') {
            navFrame.style.display = 'block';
            galleryFrame.style.width = '75%'; // Оригинальная ширина галереи
            button.style.display = 'block'
        } else {
            navFrame.style.display = 'none';
            galleryFrame.style.width = '100%'; // Галерея на весь экран
            button.style.display = 'none'
        }
    }

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
