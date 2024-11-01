

// Скролл отзывов
// Находим контейнер с отзывами
const reviewsContainer = document.getElementById('reviews-container');

// Получаем количество отзывов
const totalReviews = reviewsContainer.children.length;

console.log(totalReviews); // Вернет 6, так как у тебя 6 div'ов с классом 'review'
let currentIndex = 0;
const reviewsToShow = 2;
const reviews = document.querySelectorAll('.review');

// Функция для показа отзывов
function showReviews(index) {
    // Скрываем все отзывы
    reviews.forEach((review, i) => {
        review.style.display = 'none'; // Скрываем каждый отзыв
    });

    // Показываем только два текущих отзыва
    for (let i = index; i < index + reviewsToShow && i < reviews.length; i++) {
        reviews[i].style.display = 'block'; // Показываем отзыв
    }
}

// Инициализируем начальные отзывы
showReviews(currentIndex);

// Обработка кнопки "вправо"
document.getElementById('scroll-right').addEventListener('click', () => {
    currentIndex += 1;

    // Ограничиваем currentIndex, чтобы не допустить ситуации с показом одного отзыва
    if (currentIndex > reviews.length - reviewsToShow) {
        currentIndex = 0; // Возвращаемся в начало, если доходим до конца
    }
    showReviews(currentIndex);
});

// Обработка кнопки "влево"
document.getElementById('scroll-left').addEventListener('click', () => {
    currentIndex -= 1;

    // Ограничиваем currentIndex, чтобы не выйти за границы
    if (currentIndex < 0) {
        currentIndex = reviews.length - reviewsToShow; // Возвращаемся к последним отзывам
    }
    showReviews(currentIndex);
});




