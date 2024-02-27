document.addEventListener('DOMContentLoaded', function () {
    // Получите выпадающий список и другие элементы страницы
    var deviceDropdown = document.getElementById('deviceDropdown');
    var batteryCharge = document.getElementById('batteryCharge');
    var satelliteCount = document.getElementById('satelliteCount');
    var altitude = document.getElementById('altitude');
    var latLong = document.getElementById('latLong');
    var taserActivations = document.getElementById('taserActivations');
    var deviceLocation = document.getElementById('deviceLocation');
    var cumulativeAngle = document.getElementById('cumulativeAngle');
    var temperature = document.getElementById('temperature');
    var humidity = document.getElementById('humidity');
    var pressure = document.getElementById('pressure');
    var dateTime = document.getElementById('dateTime');

    // Обновлять данные каждые 8 секунды с задержкой в 0,0001 секунды перед первым вызовом
    setTimeout(function() {
        fetchDataAndUpdate();
        setInterval(fetchDataAndUpdate, 8000);
    }, 1);
    
    // Добавьте обработчик события изменения устройства
    deviceDropdown.addEventListener('change', function () {
        // Вызовите fetchDataAndUpdate при изменении устройства
        clearFields(); // Очистите все поля перед загрузкой новых данных
        fetchDataAndUpdate();
        
        // Сохраните выбранное устройство в локальном хранилище
        var selectedDeviceId = deviceDropdown.value;
        localStorage.setItem('lastSelectedDevice', selectedDeviceId);
    });


    // При загрузке страницы выберите последнее выбранное устройство из локального хранилища
    var lastSelectedDevice = localStorage.getItem('lastSelectedDevice');
    if (lastSelectedDevice) {
        deviceDropdown.value = lastSelectedDevice;
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

    // Функция для выполнения запроса и обновления данных
    function fetchDataAndUpdate() {
        // Получите значение выбранного устройства
        var selectedDeviceId = deviceDropdown.value;

        // Отправьте запрос на сервер для обновления данных
        fetch('/update_device_info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'device_id=' + selectedDeviceId + '&csrfmiddlewaretoken=' + getCSRFToken(),
        })
        .then(response => response.json())
        .then(data => {
            // Обновите данные на странице
            batteryCharge.textContent = data.info.battery_charge + ' %';
            satelliteCount.textContent = data.info.satellite_count + ' шт';
            latLong.textContent = data.info.latitude + ' , ' + data.info.longitude;
            dateTime.textContent = data.info.date_time;
            var deviceLocationText = data.info.inside_or_not ? 'Внутри' : 'Снаружи';
            deviceLocation.textContent = deviceLocationText;
            altitude.textContent = data.measurements[0].altitude + ' м'; 
            taserActivations.textContent = data.measurements[0].taser_activations + ' раз';
            cumulativeAngle.textContent = data.measurements[0].cumulative_angle + ' °градусов'; 
            temperature.textContent = data.measurements[0].temperature + ' °C';
            humidity.textContent = data.measurements[0].humidity + ' %'; 
            pressure.textContent = data.measurements[0].pressure + ' мм рт. ст.';            
           
        })
        .catch(error => console.error('Ошибка:', error));
    }
    // Добавьте функцию для очистки всех полей
    function clearFields() {
        batteryCharge.textContent = '';
        satelliteCount.textContent = '';
        latLong.textContent = '';
        dateTime.textContent = '';
        deviceLocation.textContent = '';
        altitude.textContent = '';
        taserActivations.textContent = '';
        cumulativeAngle.textContent = '';
        temperature.textContent = '';
        humidity.textContent = '';
        pressure.textContent = '';
    }
    
});