// Массив услуг с ценами и описанием
const services = [
    {
        category: 'Стрижка',
        items: [
            { name: 'Мужская стрижка', price: 1000, description: 'Профессиональная мужская стрижка.' },
            { name: 'Женская стрижка', price: 1500, description: 'Элегантная женская стрижка.' },
            { name: 'Детская стрижка', price: 800, description: 'Стрижка для детей до 12 лет.' }
        ]
    },
    {
        category: 'Окрашивание',
        items: [
            { name: 'Полное окрашивание', price: 3000, description: 'Полное окрашивание с качественными красителями.' },
            { name: 'Омбре', price: 3500, description: 'Модное окрашивание омбре.' },
            { name: 'Мелирование', price: 2500, description: 'Частичное мелирование для освежения образа.' },
            { name: 'Тонирование', price: 2000, description: 'Тонирование для улучшения цвета волос.' }
        ]
    },
    {
        category: 'Маникюр',
        items: [
            { name: 'Классический маникюр', price: 1200, description: 'Классический маникюр с уходом за кожей.' },
            { name: 'Французский маникюр', price: 1400, description: 'Элегантный французский маникюр.' },
            { name: 'Аппаратный маникюр', price: 1500, description: 'Современный аппаратный маникюр.' },
            { name: 'Дизайн ногтей', price: 1800, description: 'Уникальный дизайн на ногтях.' }
        ]
    },
    {
        category: 'Педикюр',
        items: [
            { name: 'Классический педикюр', price: 1500, description: 'Классический уход за ногами.' },
            { name: 'Аппаратный педикюр', price: 1700, description: 'Современный аппаратный педикюр.' },
            { name: 'Педикюр с покрытием', price: 2000, description: 'Уход за ногами с покрытием.' }
        ]
    },
    {
        category: 'Массаж',
        items: [
            { name: 'Классический массаж', price: 3000, description: 'Расслабляющий классический массаж всего тела.' },
            { name: 'Массаж спины', price: 2000, description: 'Целевой массаж спины для снятия напряжения.' },
            { name: 'Ароматерапия', price: 3500, description: 'Массаж с использованием эфирных масел.' }
        ]
    },
    {
        category: 'Уход за лицом',
        items: [
            { name: 'Чистка лица', price: 2500, description: 'Глубокая чистка лица с уходом за кожей.' },
            { name: 'Пилинг', price: 3000, description: 'Эксфолиация для обновления кожи.' },
            { name: 'Маска для лица', price: 1200, description: 'Увлажняющая маска для лица.' },
            { name: 'Антивозрастная процедура', price: 4000, description: 'Процедура для омоложения кожи.' }
        ]
    }
];


// Массив специалистов с аватарками и описанием
const masters = [
    {
        name: 'Анна Иванова',
        avatar: 'anna.jpg',
        description: 'Специалист по стрижкам и окрашиванию с 10-летним опытом.',
        categories: ['Стрижка', 'Окрашивание'],
        schedule: [
            { date: '2024-10-20', times: ['10:00', '11:00', '12:00'] },
            { date: '2024-10-21', times: ['13:00', '14:00'] }
        ]
    },
    {
        name: 'Олег Смирнов',
        avatar: 'oleg.jpg',
        description: 'Мастер по маникюру и педикюру с большим стажем.',
        categories: ['Маникюр', 'Педикюр'],
        schedule: [
            { date: '2024-10-20', times: ['09:00', '10:00', '11:00'] },
            { date: '2024-10-21', times: ['12:00', '13:00'] }
        ]
    },
    {
        name: 'Мария Петрова',
        avatar: 'maria.jpg',
        description: 'Мастер по косметическим процедурам и массажу.',
        categories: ['Массаж', 'Уход за лицом'],
        schedule: [
            { date: '2024-10-20', times: ['12:00', '14:00', '15:00'] },
            { date: '2024-10-21', times: ['09:00', '10:00'] }
        ]
    },
    {
        name: 'Ирина Федорова',
        avatar: 'irina.jpg',
        description: 'Мастер по маникюру',
        categories: ['Маникюр'],
        schedule: [
            { date: '2024-10-20', times: ['12:00', '14:00', '15:00'] },
            { date: '2024-10-25', times: ['09:00', '10:00'] }
        ]
    },
    {
        name: 'Екатерина Соколова',
        avatar: 'ekaterina.jpg',
        description: 'Специалист по окрашиванию',
        categories: ['Окрашивание'],
        schedule: [
            { date: '2024-10-20', times: ['12:00', '14:00', '15:00'] },
            { date: '2024-10-21', times: ['09:00', '10:00'] }
        ]
    },
    {
        name: 'Владимир Мельников',
        avatar: 'vladimir.jpg',
        description: 'Профессиольный парикмахер',
        categories: ['Стрижка'],
        schedule: [
            { date: '2024-10-20', times: ['12:00', '14:00', '15:00'] },
            { date: '2024-10-21', times: ['09:00', '10:00'] }
        ]
    },
];

// Переменные для выбранной услуги и мастера
let selectedService = null;
let selectedMaster = null;
let selectedServicePrice = null;

window.onload = function() {
        document.getElementById('auth-modal').style.display = 'block';
    };

// Функция для переключения вкладок
function openTab(event, tabId) {
    const tabs = document.getElementsByClassName('tab-content');
    const buttons = document.getElementsByClassName('tab-button');

    // Скрыть все вкладки и убрать класс "active" с кнопок
    for (let tab of tabs) {
        tab.classList.remove('active');
    }
    for (let button of buttons) {
        button.classList.remove('active');
    }

    // Показать выбранную вкладку и установить ее активной
    document.getElementById(tabId).classList.add('active');

    // Если вызов идет от кнопки, event может быть null, тогда активируем правильную вкладку вручную
    if (event) {
        event.currentTarget.classList.add('active');
    } else {
        // Ищем кнопку по связанному с вкладкой tabId
        const targetButton = Array.from(buttons).find(button => button.getAttribute('onclick').includes(tabId));
        if (targetButton) {
            targetButton.classList.add('active');
        }
    }

    // Дополнительные действия при переключении на вкладку
    if (tabId === 'master-tab') {
        showMasterTab();
    } else if (tabId === 'time-tab') {
        showTimeTab();
    }
}


// Показываем список услуг в зависимости от выбранной категории
function showServices(category) {
    const servicesList = services.find(service => service.category === category).items;
    let servicesDetails = servicesList.map(service =>
        `<p class="service-item" onclick="selectService(this)">
            ${service.name} - ${service.price} руб.<br>
            <small>${service.description}</small>
        </p>`
    ).join('');
    document.getElementById('services-details').innerHTML = servicesDetails;
    selectedService = null;
    document.getElementById('services-next').disabled = true;
    document.getElementById('error-message').innerText = ''; // Убираем сообщение об ошибке
}

// Функция для выбора услуги
function selectService(serviceElement) {
    const allServices = document.getElementsByClassName('service-item');
    for (let service of allServices) {
        service.classList.remove('selected');
    }
    serviceElement.classList.add('selected');

    // Получаем название и цену выбранной услуги
    const serviceText = serviceElement.textContent.split(' - ');
    selectedService = serviceText[0].trim();  // Название услуги
    selectedServicePrice = serviceText[1].split(' ')[0].trim();  // Цена услуги

    // Сброс мастера и времени при выборе новой услуги
    selectedMaster = null;
    document.getElementById('master-list').innerHTML = ''; // Очищаем список мастеров
    document.getElementById('time').innerHTML = '<option value="">--Выберите время--</option>'; // Очищаем время
    document.getElementById('master-next').disabled = true; // Деактивируем кнопку "Далее"

    console.log("Выбранная услуга:", selectedService, "Цена:", selectedServicePrice); // Отладка

    document.getElementById('services-next').disabled = false;
    document.getElementById('error-message').innerText = '';

    const selectedCategory = services.find(service =>
        service.items.some(item => item.name === selectedService));

    if (selectedCategory) {
        filterMastersByServiceCategory(selectedCategory.category);
        updateSelectedServiceMaster();
    }
}


// Фильтрация мастеров по категории услуг
function filterMastersByServiceCategory(category) {
    console.log("Фильтрация мастеров для категории:", category); // Отладка

    const filteredMasters = masters.filter(master => master.categories.includes(category));

    // Выводим результат фильтрации в консоль
    console.log("Найденные мастера:", filteredMasters);

    let masterList = filteredMasters.map(master =>
        `<li class="master-item" onclick="selectMaster(this)">
            <img src="${master.avatar}" alt="${master.name}" class="avatar">
            <div class="master-info">
                <strong>${master.name}</strong><br>
                ${master.description}
            </div>
        </li>`
    ).join('');

    // Если список мастеров пустой, выводим сообщение
    if (!filteredMasters.length) {
        console.log("Мастера для данной категории не найдены.");
    }

    document.getElementById('master-list').innerHTML = masterList;
}


// Функция выбора мастера
function selectMaster(masterElement) {
    const allMasters = document.getElementsByClassName('master-item');
    for (let master of allMasters) {
        master.classList.remove('selected');
    }
    masterElement.classList.add('selected');
    selectedMaster = masterElement.querySelector('.master-info strong').textContent.trim(); // Сохранить выбранного мастера

    document.getElementById('master-next').disabled = false; // Активировать кнопку "Далее"
    document.getElementById('time').innerHTML = '<option value="">--Выберите время--</option>'; // Очищаем список времени

    populateAvailableTimes(); // Обновляем даты и время для выбранного мастера
    updateSelectedServiceMaster()
}



// Функция обновления доступных дат и времени для выбранного мастера
function populateAvailableTimes() {
    const dateSelect = document.getElementById('date');
    const timeSelect = document.getElementById('time');

    // Очищаем предыдущие данные
    dateSelect.innerHTML = '';
    timeSelect.innerHTML = '<option value="">--Выберите время--</option>';

    // Проверяем, выбран ли мастер
    if (!selectedMaster) {
        return;
    }

    // Найти расписание для выбранного мастера
    const selectedMasterData = masters.find(master => master.name === selectedMaster);

    if (selectedMasterData && selectedMasterData.schedule) {
        // Генерация доступных дат
        selectedMasterData.schedule.forEach(item => {
            const option = document.createElement('option');
            option.value = item.date;
            option.textContent = item.date;
            dateSelect.appendChild(option);
        });
    }
}

// Обновление времени на основе выбранной даты
document.getElementById('date').addEventListener('change', function() {
    const selectedDate = this.value;
    const timeSelect = document.getElementById('time');
    timeSelect.innerHTML = ''; // Очищаем предыдущие значения

    const availableTime = availableDates.find(item => item.date === selectedDate);
    if (availableTime) {
        availableTime.times.forEach(time => {
            const option = document.createElement('option');
            option.value = time;
            option.textContent = time;
            timeSelect.appendChild(option);
        });
    }
});

// Поиск мастеров по ФИО
function searchMasters() {
    const input = document.getElementById('search-master').value.toLowerCase();
    const mastersList = document.getElementsByClassName('master-item');

    for (let master of mastersList) {
        const name = master.textContent.toLowerCase();
        if (name.includes(input)) {
            master.style.display = ''; // Показать элемент
        } else {
            master.style.display = 'none'; // Скрыть элемент
        }
    }
}

// Проверка кнопки "Далее" для вкладки Услуги
document.getElementById('services-next').onclick = function(event) {
    if (!selectedService) {
        document.getElementById('error-message').innerText = 'Пожалуйста, выберите услугу!';
    } else {
        openTab(null, 'master-tab'); // Переключение на вкладку мастеров
        document.getElementById('error-message').innerText = ''; // Убираем сообщение об ошибке
    }
};

// Проверка кнопки "Далее" для вкладки Мастеры
document.getElementById('master-next').onclick = function(event) {
    if (!selectedMaster) {
        document.getElementById('master-error-message').innerText = 'Пожалуйста, выберите мастера!';
    } else {
        openTab(null, 'time-tab'); // Переключение на вкладку времени
        document.getElementById('master-error-message').innerText = ''; // Убираем сообщение об ошибке
    }
};


// Если услуга не выбрана - выводим сообщение
function showMasterTab() {
    if (!selectedService) {
        document.getElementById('master-list').innerHTML = '<p style="color: red; text-align: center; font-size: 15px; font-weight: bold;">Услуга не выбрана</p>';
        document.getElementById('master-next').disabled = true;
    } else {
        filterMastersByServiceCategory(services.find(service => service.items.some(item => item.name === selectedService)).category);
    }
}

// Обновляем список времени только если мастер выбран
document.getElementById('date').addEventListener('change', function() {
    const selectedDate = this.value;
    const timeSelect = document.getElementById('time');

    // Очищаем список времени
    timeSelect.innerHTML = '<option value="">--Выберите время--</option>';

    // Проверяем, выбран ли мастер
    if (!selectedMaster) {
        timeSelect.innerHTML = '<option value="">Мастер не выбран</option>';
        document.getElementById('book-btn').disabled = true;
        return; // Если мастер не выбран, выходим из функции, чтобы не продолжать
    }

    // Найти расписание выбранного мастера для выбранной даты
    const selectedMasterData = masters.find(master => master.name === selectedMaster);
    const availableTimes = selectedMasterData.schedule.find(item => item.date === selectedDate);

    if (availableTimes) {
        availableTimes.times.forEach(time => {
            const option = document.createElement('option');
            option.value = time;
            option.textContent = time;
            timeSelect.appendChild(option);
        });
    }

    checkBookingButton(); // Проверяем, можно ли активировать кнопку "Записаться"
});



// Функция для обновления информации на вкладке "Время"
function showTimeTab() {
    const dateSelect = document.getElementById('date');
    const timeSelect = document.getElementById('time');
    const timeTabMessage = document.getElementById('time-tab-message');
    const servicePriceElement = document.getElementById('service-price');  // Элемент для отображения цены

    // Если не выбрана услуга или мастер, выводим сообщение и скрываем поля выбора даты и времени
    if (!selectedService || !selectedMaster) {
        timeTabMessage.innerText = 'Выберите мастера';  // Выводим сообщение
        dateSelect.style.display = 'none';  // Скрываем выбор даты
        timeSelect.style.display = 'none';  // Скрываем выбор времени
        servicePriceElement.innerText = '';  // Очищаем отображение цены
    } else {
        // Если мастер и услуга выбраны, показываем выбор даты и времени
        timeTabMessage.innerText = '';  // Очищаем сообщение
        dateSelect.style.display = 'block';  // Показываем выбор даты
        timeSelect.style.display = 'block';  // Показываем выбор времени
        servicePriceElement.innerText = `Стоимость услуги: ${selectedServicePrice} руб.`;  // Отображаем цену
        populateAvailableTimes();  // Обновляем доступные даты и время
    }

    // Независимо от состояния мастера или услуги, кнопка "Записаться" и текст с выбранной информацией остаются видимыми
    document.getElementById('book-btn').style.display = 'block';  // Кнопка всегда видна
    document.getElementById('selected-service-master').style.display = 'block';  // Текст о выбранной услуге и мастере виден
}

// Активация кнопки "Записаться", если выбраны дата и время
document.getElementById('date').addEventListener('change', function() {
    checkBookingButton();
});

document.getElementById('time').addEventListener('change', function() {
    checkBookingButton();
});

// Проверка возможности активации кнопки "Записаться"
function checkBookingButton() {
    const selectedDate = document.getElementById('date').value;
    const selectedTime = document.getElementById('time').value;

    // Кнопка активируется только если выбраны дата, время и мастер
    document.getElementById('book-btn').disabled = !(selectedDate && selectedTime && selectedMaster);
}

// Логика записи
document.getElementById('book-btn').onclick = function() {
    const selectedDate = document.getElementById('date').value;
    const selectedTime = document.getElementById('time').value;

    if (selectedDate && selectedTime && selectedMaster) {
        alert(`Вы успешно записались на услугу: ${selectedService}, мастер: ${selectedMaster}, дата: ${selectedDate}, время: ${selectedTime}`);
    }
};


function updateSelectedServiceMaster() {
    const selectedServiceMaster = document.getElementById('selected-service-master');
    selectedServiceMaster.textContent = `Вы выбрали услугу: ${selectedService || 'не выбрано'}. Мастер: ${selectedMaster || 'не выбрано'}`;
}


// Вызываем функции при загрузке страницы
window.onload = function() {
    updateSelectedServiceMaster()
    populateAvailableTimes();
    showTimeTab()
};