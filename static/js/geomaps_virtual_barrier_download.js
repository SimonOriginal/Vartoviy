const map = L.map('map').setView([48.350427, 16.417968], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const drawnItems = new L.FeatureGroup();

// Добавьте обработчик события изменения устройства
deviceDropdown.addEventListener('change', function () {
    // Сохраните выбранное устройство в локальном хранилище
    PointView();
    var selectedDeviceId = deviceDropdown.value;
    localStorage.setItem('lastSelectedDevice', selectedDeviceId);
});

// При загрузке страницы выберите последнее выбранное устройство из локального хранилища
var lastSelectedDevice = localStorage.getItem('lastSelectedDevice');
if (lastSelectedDevice) {
    deviceDropdown.value = lastSelectedDevice;
}

map.addLayer(drawnItems);

function fitBoundsToGeoJSON(geoJSON) {
    const bounds = L.geoJSON(geoJSON).getBounds();
    map.fitBounds(bounds);
}

let geoJSONData = null; // Переменная для хранения GeoJSON данных

// Получение CSRF-токена из cookies
function getCSRFToken() {
    var csrfToken = null;
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === 'csrftoken=') {
            csrfToken = decodeURIComponent(cookie.substring(10));
            break;
        }
    }
    return csrfToken;
}

function fetchDataAndUpdate() {
    // Получите значение выбранного устройства
    var selectedDeviceId = deviceDropdown.value;

    // Отправьте запрос на сервер для обновления данных
    fetch('/configuration/get_geojson/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),  // Include CSRF token in headers
        },
        body: 'device_id=' + encodeURIComponent(selectedDeviceId),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Ошибка при получении данных с сервера.');
        }
    })
    .then(data => {
        if (data.geojson) {
            // Parse the GeoJSON string into a JSON object
            const geoJSONData = JSON.parse(data.geojson);

            // Assuming you want to handle the first feature in the GeoJSON
            const firstFeature = geoJSONData.features[0];

            // Очищаем предыдущие слои и добавляем новый слой на карту
            drawnItems.clearLayers();
            L.geoJSON(firstFeature, {
                onEachFeature: function (feature, layer) {
                    drawnItems.addLayer(layer);
                }
            }).addTo(map);

             // Вызываем функцию, чтобы подогнать карту под границы геозоны
            fitBoundsToGeoJSON(firstFeature);
        } else {
            console.error('Сервер не вернул данные о геозонах.');
        }
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}

// Обновлять данные каждые 8 секунды с задержкой в 0,0001 секунды перед первым вызовом
setTimeout(function() {
    PointView();
    setInterval(PointView, 8000);
}, 1);

// Функция для выполнения запроса и обновления данных
function PointView() {
    // Получите значение выбранного устройства
    var selectedDeviceId = deviceDropdown.value;

    // Отправьте запрос на сервер для обновления данных
    fetch('/point/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'device_id=' + selectedDeviceId + '&csrfmiddlewaretoken=' + getCSRFToken(),
    })
    .then(response => response.json())
    .then(data => {
        // Обновите данные на странице
        latLong.textContent = data.info.latitude + ' , ' + data.info.longitude;
        dateTime.textContent = data.info.date_time;

        // Очистите все маркеры на карте
        map.eachLayer(layer => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        // Добавьте новый маркер на карту
        var marker = L.marker([data.info.latitude, data.info.longitude]).addTo(map);
        // Обработчик события клика на маркере
        marker.on('click', function (e) {
            // Получение координат маркера
            var latlng = marker.getLatLng();
            
            // Отображение координат в консоли (вы можете изменить это на вашу логику обработки координат)
            console.log("Координаты: " + latlng.lat + ", " + latlng.lng);
        });

        // Пример использования попапа для отображения координат при клике на маркере
        marker.bindPopup("Координаты: " + data.info.latitude + ", " + data.info.longitude);

    })
    .catch(error => console.error('Ошибка:', error));
}

// Вызываем функцию загрузки данных и добавления слоя после загрузки страницы
document.addEventListener('DOMContentLoaded', function () {
    const deviceDropdown = document.getElementById('deviceDropdown');

    // Обработчик события изменения выбранного устройства
    deviceDropdown.addEventListener('change', fetchDataAndUpdate);

    // Загрузка данных при загрузке страницы для выбранного устройства
    fetchDataAndUpdate();
});