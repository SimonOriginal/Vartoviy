var map = L.map('map').setView([49.55, 7.32], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(map);

var markers = L.layerGroup().addTo(map);
var line = L.layerGroup().addTo(map);

var autoRefreshCheckbox = document.getElementById('autoRefreshCheckbox');
var polyline;
var previousData = []; // Добавляем переменную для хранения предыдущих данных
var clickCounter = 0; // Счетчик кликов

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

// Добавляем обработчик события для изменения состояния чекбокса
autoRefreshCheckbox.addEventListener('change', function () {
    // Сохраняем состояние чекбокса в локальное хранилище
    var autoRefreshState = autoRefreshCheckbox.checked;
    localStorage.setItem('autoRefreshState', autoRefreshState);

    // Проверяем состояние чекбокса и соответственно обновляем карту или приближаемся к маркеру
    if (autoRefreshState) {
        getData();
    } else {
        map.fitBounds(polyline.getBounds());
    }
});

// При загрузке страницы выбираем последнее сохраненное состояние чекбокса из локального хранилища
var lastAutoRefreshState = localStorage.getItem('autoRefreshState');
if (lastAutoRefreshState !== null) {
    autoRefreshCheckbox.checked = JSON.parse(lastAutoRefreshState);
}

var maxDataPointsSlider = document.getElementById('maxDataPointsSlider');
var maxDataPointsValue = document.getElementById('maxDataPointsValue');

let timeoutId;

maxDataPointsSlider.addEventListener('input', function () {
    // Отменяем предыдущий таймаут, если он существует
    clearTimeout(timeoutId);
    maxDataPointsValue.textContent = maxDataPointsSlider.value;

    // Устанавливаем новый таймаут
    timeoutId = setTimeout(function () {
        localStorage.setItem('maxDataPoints', maxDataPointsSlider.value);
        getData();
    }, 1000);
});


var savedMaxDataPoints = localStorage.getItem('maxDataPoints');
if (savedMaxDataPoints !== null) {
    maxDataPointsSlider.value = savedMaxDataPoints;
    maxDataPointsValue.textContent = savedMaxDataPoints;
}

function getData() {
    var selectedDevice = document.getElementById('deviceDropdown').value;

    fetch(`/journeylog/get_data/${selectedDevice}/`)
        .then(response => response.json())
        .then(data => {
            // Сначала очистите все слои, чтобы начать с чистого листа
            markers.clearLayers();

            var maxDataPoints = maxDataPointsSlider.value;
            // Оставьте только нужное количество точек
            data = data.slice(-maxDataPoints);

            // Потом добавьте новые точки
            for (let point of data) {
                let marker = L.marker([point.lat, point.lng]).bindPopup(`Latitude: ${point.lat}<br>Longitude: ${point.lng}<br>${point.time}`);
                markers.addLayer(marker);
            }

            // Остальной код остается без изменений
            if (polyline) {
                polyline.setLatLngs(data.map(p => [p.lat, p.lng]));
            } else {
                polyline = L.polyline(data.map(p => [p.lat, p.lng]), {color: 'blue'}).addTo(line);
            }

            if (autoRefreshCheckbox.checked) {
                var lastPoint = markers.getLayers().pop();
                if (lastPoint) {
                    var currentZoom = map.getZoom();
                    var targetZoom = (currentZoom === 18) ? 18 : 18;

                    map.flyTo(lastPoint.getLatLng(), targetZoom, {
                        duration: 2
                    });
                }
            } else {
                map.fitBounds(polyline.getBounds());
            }

            previousData = data;
        })
        .catch(error => console.error(error));
}

window.onload = getData;
document.getElementById('deviceDropdown').addEventListener('change', getData);


document.getElementById('refreshDataButton').addEventListener('click', function () {
    getData();
});

document.getElementById('getLocationPointButton').addEventListener('click', function () {
  var lastPoint = markers.getLayers().pop();

  if (lastPoint) {
      clickCounter++;

      if (clickCounter === 1) {
          // При первом клике перемещаемся к последней точке
          var currentZoom = map.getZoom();
          var targetZoom = (currentZoom === 18) ? 5 : 18;

          map.setView(lastPoint.getLatLng(), targetZoom);
      } else if (clickCounter === 2) {
          // При втором клике изменяем масштаб для обзора всех точек
          map.fitBounds(polyline.getBounds());
      } else if (clickCounter === 3) {
          // При третьем клике возвращаемся к изначальному виду
          map.setView([49.55, 7.32], 4);
          clickCounter = 0;
      }
  }
});

// Добавляем обработчик события для изменения состояния чекбокса
autoRefreshCheckbox.addEventListener('change', function () {
    // Проверяем состояние чекбокса и соответственно обновляем карту или приближаемся к маркеру
    if (autoRefreshCheckbox.checked) {
        getData();
    } else {
        map.fitBounds(polyline.getBounds());
    }
});

// Устанавливаем интервал для автоматического обновления данных каждые 8 секунд
setInterval(function () {
    if (autoRefreshCheckbox.checked) {
        getData();
    }
}, 8000);
