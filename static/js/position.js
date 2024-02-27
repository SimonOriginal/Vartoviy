// Функция для изменения иконки и добавления индикатора загрузки
function setLoadingState() {
    const locationIcon = document.getElementById('locationIcon');
    locationIcon.classList.remove('fa-street-view');
    locationIcon.classList.add('fa-spinner', 'fa-spin');

    setTimeout(() => {
        // Возвращаем исходную иконку через 5 секунд
        locationIcon.classList.remove('fa-spinner', 'fa-spin');
        locationIcon.classList.add('fa-street-view');
    }, 5000);
}

// Функция для обработки успешного получения местоположения
function showLocation(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Очищаем результат и возвращаем исходную иконку
    const locationIcon = document.getElementById('locationIcon');
    locationIcon.classList.remove('fa-spinner', 'fa-spin');
    locationIcon.classList.add('fa-street-view');

    // Создаем маркер для местоположения пользователя
    const userLocationMarker = L.marker([latitude, longitude]).addTo(map);
    userLocationMarker.bindPopup(`Ваше местоположение: <br> Широта: ${latitude.toFixed(6)}, <br> Долгота: ${longitude.toFixed(6)}`).openPopup();

    // Перемещаем карту к местоположению пользователя
    map.setView([latitude, longitude], 15);
}

// Функция для обработки ошибки получения местоположения
function handleLocationError(error) {
    const locationIcon = document.getElementById('locationIcon');
    locationIcon.classList.remove('fa-spinner', 'fa-spin');
    locationIcon.classList.add('fa-triangle-exclamation');
}

// Функция для определения местоположения пользователя
function getLocation() {
    setLoadingState();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showLocation, handleLocationError);
    } else {
        // Уведомление о том, что геолокация не поддерживается
        alert('Геолокация не поддерживается вашим браузером.');
    }
}

// Добавляем обработчик события для кнопки определения местоположения
document.getElementById('getLocationButton').addEventListener('click', getLocation);
