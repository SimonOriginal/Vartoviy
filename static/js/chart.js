document.addEventListener('DOMContentLoaded', function () {
    // Получаем элементы canvas
    var batteryCanvas = document.getElementById('batteryChart').getContext('2d');
    var satelliteCanvas = document.getElementById('satelliteChart').getContext('2d');
    var insideCanvas = document.getElementById('insideChart').getContext('2d');
    var cumulativeAngleCanvas = document.getElementById('cumulativeAngleChart').getContext('2d');
    var pressureCanvas = document.getElementById('pressureChart').getContext('2d');
    var altitudeCanvas = document.getElementById('altitudeChart').getContext('2d');
    var temperatureCanvas = document.getElementById('temperatureChart').getContext('2d');
    var humidityCanvas = document.getElementById('humidityChart').getContext('2d');
    var taserActivationsCanvas = document.getElementById('taserActivationsChart').getContext('2d');

    // Создаем пустые графики
    var batteryChart = createChart(batteryCanvas, 'Battery Charge', [], []);
    var satelliteChart = createChart(satelliteCanvas, 'Satellite Count', [], []);
    var insideChart = createChart(insideCanvas, 'Inside or Not', [], []);
    var cumulativeAngleChart = createChart(cumulativeAngleCanvas, 'Cumulative Angle', [], []);
    var pressureChart = createChart(pressureCanvas, 'Pressure', [], []);
    var altitudeChart = createChart(altitudeCanvas, 'Altitude', [], []);
    var temperatureChart = createChart(temperatureCanvas, 'Temperature', [], []);
    var humidityChart = createChart(humidityCanvas, 'Humidity', [], []);
    var taserActivationsChart = createChart(taserActivationsCanvas, 'Taser Activations', [], []);
    // ... (повторите для остальных графиков)

    // Получаем элементы слайдера
    var maxDataPointsSlider = document.getElementById('maxDataPointsSlider');
    var maxDataPointsValue = document.getElementById('maxDataPointsValue');

    // Функция для создания пустого графика с использованием Chart.js
    function createChart(canvas, label, labels, data) {
        return new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: [{
                        type: 'time',
                        time: {
                            unit: 'day'
                        }
                    }],
                    y: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    // Функция для обновления графиков
    function updateCharts() {
        var deviceDropdown = document.getElementById('deviceDropdown');
        var deviceId = deviceDropdown.value;

        var maxDataPoints = maxDataPointsSlider.value;

        fetch('/charts/', {
            method: 'POST',
            body: JSON.stringify({ device_id: deviceId }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            }
        })
        .then(response => response.json())
        .then(data => {
            // Обновляем данные графика
            updateChart(batteryChart, data.labels, data.battery_charge);
            updateChart(satelliteChart, data.labels, data.satellite_count);
            updateChart(insideChart, data.labels, data.inside_or_not);
            updateChart(cumulativeAngleChart, data.labels, data.cumulative_angle);
            updateChart(pressureChart, data.labels, data.pressure);
            updateChart(altitudeChart, data.labels, data.altitude);
            updateChart(temperatureChart, data.labels, data.temperature);
            updateChart(humidityChart, data.labels, data.humidity);
            updateChart(taserActivationsChart, data.labels, data.taser_activations);
            // ... (повторите для остальных графиков)
        })
        .catch(error => console.error('Error:', error));
    }

    // Функция для обновления данных графика
    function updateChart(chart, labels, data) {
        var maxDataPoints = maxDataPointsSlider.value;

        // Обновляем значение слайдера визуально
        maxDataPointsValue.textContent = maxDataPoints;

        // Обновляем данные графика
        chart.data.labels = labels.slice(-maxDataPoints);
        chart.data.datasets[0].data = data.slice(-maxDataPoints);
        chart.update();
    }

    // Вызываем функцию при загрузке страницы
    updateCharts();

    // Обновляем графики каждые 8 секунд
    setInterval(updateCharts, 8000);

    // Добавляем обработчик события изменения значения выпадающего списка
    var deviceDropdown = document.getElementById('deviceDropdown');
    deviceDropdown.addEventListener('change', function () {
        // При изменении выбора устройства вызываем обновление графиков
        updateCharts();
    });

    // Добавляем обработчик события изменения значения слайдера
    let timeoutId;

    maxDataPointsSlider.addEventListener('input', function () {
        // Обновляем значение визуально
        maxDataPointsValue.textContent = maxDataPointsSlider.value;

        // Отменяем предыдущий таймаут, если он существует
        clearTimeout(timeoutId);

        // Устанавливаем новый таймаут
        timeoutId = setTimeout(function () {
            // При изменении значения слайдера вызываем обновление графиков
            updateCharts();
        }, 1000);
    });

});