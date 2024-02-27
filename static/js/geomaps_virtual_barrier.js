const map = L.map('map').setView([48.350427, 16.417968], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Добавьте обработчик события изменения устройства
deviceDropdown.addEventListener('change', function () {
    // Сохраните выбранное устройство в локальном хранилище
    var selectedDeviceId = deviceDropdown.value;
    localStorage.setItem('lastSelectedDevice', selectedDeviceId);
});

// При загрузке страницы выберите последнее выбранное устройство из локального хранилища
var lastSelectedDevice = localStorage.getItem('lastSelectedDevice');
if (lastSelectedDevice) {
    deviceDropdown.value = lastSelectedDevice;
}

const drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        poly: {
            allowIntersection: false
        }
    },
    draw: {
        polygon: {
            allowIntersection: false,
            showArea: true
        },
        marker: false,
        circlemarker: false,
        polyline: false,
        rectangle: true,
        circle: false
    }
});

function fitBoundsToGeoJSON(geoJSON) {
    const bounds = L.geoJSON(geoJSON).getBounds();
    map.fitBounds(bounds);
}


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
    
                // Отображаем координаты в консоли
                if (firstFeature.geometry && firstFeature.geometry.coordinates && firstFeature.geometry.coordinates.length > 0) {
                    const coordinates = firstFeature.geometry.coordinates[0];
                    const formattedCoordinates = coordinates.map(coord => ({
                        Latitude: coord[1].toFixed(6),
                        Longitude: coord[0].toFixed(6)
                    }));
                    console.table(formattedCoordinates);
    
                    // Форматируем и отображаем координаты первой геозоны в текстовом поле
                    const consoleOutput = coordinates.map(coord => {
                        const lat = coord[1].toFixed(6); // Широта
                        const lng = coord[0].toFixed(6); // Долгота
                        return `\tШирота: ${lat}, Долгота: ${lng}\n`; // Добавляем отступ и символ новой строки
                    }).join('');
    
                    document.getElementById('console').value = consoleOutput;
                } else {
                    console.error('GeoJSON данные не содержат координат.');
                }
            } else {
                console.error('Сервер не вернул данные о геозонах.');
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
    }
    
    // Вызываем функцию загрузки данных и добавления слоя после загрузки страницы
    document.addEventListener('DOMContentLoaded', function () {
        const deviceDropdown = document.getElementById('deviceDropdown');
    
        // Обработчик события изменения выбранного устройства
        deviceDropdown.addEventListener('change', fetchDataAndUpdate);
    
        // Загрузка данных при загрузке страницы для выбранного устройства
        fetchDataAndUpdate();
    });    

map.addControl(drawControl);

map.on('draw:created', function (event) {
    const layer = event.layer;
    drawnItems.addLayer(layer);
    const geoJSONData = layer.toGeoJSON();
    const coordinates = geoJSONData.geometry.coordinates[0];

    // Формируем массив объектов с отформатированными координатами
    const formattedCoordinates = coordinates.map(coord => {
        const lat = parseFloat(coord[1].toFixed(6)); // Широта
        const lng = parseFloat(coord[0].toFixed(6)); // Долгота
        return { Latitude: lat, Longitude: lng };
    });

    // Выводим отформатированные данные в консоль в виде таблицы
    console.table(formattedCoordinates);

    // Форматируем и отображаем координаты первой геозоны в текстовом поле
    const consoleOutput = coordinates.map(coord => {
        const lat = coord[1].toFixed(6); // Широта
        const lng = coord[0].toFixed(6); // Долгота
        return `\tШирота: ${lat}, Долгота: ${lng}\n`; // Добавляем отступ и символ новой строки
    }).join('');
    
    document.getElementById('console').value = consoleOutput;
    
});

// Функция для обновления данных в консоли
function updateConsoleData() {
    const layers = drawnItems.getLayers();
    if (layers.length > 0) {
        const geoJSONData = layers[0].toGeoJSON(); // Предполагаем, что у вас есть только один слой
        const coordinates = geoJSONData.geometry.coordinates[0];

        // Форматируем и выводим координаты геозоны в консоль
        const consoleOutput = coordinates.map(coord => {
            const lat = coord[1].toFixed(6); // Широта
            const lng = coord[0].toFixed(6); // Долгота
            return `\tШирота: ${lat}, Долгота: ${lng}\n`; // Добавляем отступ и символ новой строки
        }).join('');

        document.getElementById('console').innerText = consoleOutput;
    } else {
        document.getElementById('console').innerText = '';
    }
}

// Обработчик события при создании новой геозоны
map.on('draw:created', function (event) {
    drawnItems.clearLayers(); // Удаляем предыдущие геозоны
    const layer = event.layer;
    drawnItems.addLayer(layer);
    updateConsoleData();
});

window.onload = function() {
    document.getElementById('console').value = ''; // Очищаем содержимое консоли при загрузке страницы
};

// Обработчик события при удалении геозоны
map.on('draw:deleted', function (event) {
    document.getElementById('console').value = ''; // Очищаем содержимое консоли
});

// Найти кнопку по ее id и добавить обработчик события для нажатия
const copyButton = document.getElementById('copy-button');
copyButton.addEventListener('click', copyToClipboard);

// Функция для копирования текста из текстового поля в буфер обмена
function copyToClipboard() {
    const textarea = document.getElementById('console');
    textarea.focus();
    textarea.setSelectionRange(0, textarea.value.length); // Устанавливаем выделение для всего текста в поле
    document.execCommand('copy'); // Копируем текст в буфер обмена
    textarea.setSelectionRange(0, 0); // Убираем выделение текста
}


// Загрузка GeoJSON по нажатию кнопки
document.getElementById('downloadGeoJSON').addEventListener('click', function () {
    const data = drawnItems.toGeoJSON();
    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'geofence.geojson';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
});

document.getElementById('copy-button').addEventListener('click', function () {
    var button = this;
    var icon = button.querySelector('i');

    // После успешного копирования меняем иконку на галочку
    icon.classList.remove('far', 'fa-copy');
    icon.classList.add('fas', 'fa-check');

    // Опционально: установите таймер для возврата исходной иконки
    setTimeout(function () {
        icon.classList.remove('fas', 'fa-check');
        icon.classList.add('far', 'fa-copy');
    }, 3000); // Вернуть исходную иконку через 3 секунды
});

function playAnimation(animationTarget, animationName) {
    anime({
        targets: animationTarget,
        easing: 'easeInOutQuad',
        duration: 1000,
        backgroundColor: ['#ff6f61', '#6c757d'],
        scale: [1, 1.1, 1],
        direction: 'alternate',
        loop: false
    });
}

document.getElementById('saveGeoJSONToDatabase').addEventListener('click', function () {
    const button = this; // Сохраняем ссылку на кнопку в переменной
    const originalIcon = button.innerHTML; // Сохраняем оригинальный HTML содержимое кнопки

    const data = drawnItems.toGeoJSON();
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const selectedDeviceId = document.getElementById('deviceDropdown').value;  // Assuming you have a device dropdown

    fetch('/configuration/save_geozone/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            geojson: JSON.stringify(data),
            name: 'geozone',
            device_id: selectedDeviceId
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('Геозона успешно сохранена в базу данных!');
            button.innerHTML = '<i class="fas fa-check"></i> Геозона сохранена';
        } else {
            console.error('Ошибка при сохранении геозоны в базу данных.');
            button.innerHTML = '<i class="fas fa-times"></i> Ошибка сохранения';
        }

        // Через 3 секунды вернуть кнопке оригинальную иконку
        setTimeout(function () {
            button.innerHTML = originalIcon;
        }, 3000);
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
        button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Произошла ошибка';
        
        // Через 3 секунды вернуть кнопке оригинальную иконку
        setTimeout(function () {
            button.innerHTML = originalIcon;
        }, 3000);
    });
});
