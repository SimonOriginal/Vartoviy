$(document).ready(function () {
    var currentPageInfo = 1;
    var currentPageMeasurements = 1;

    // Вызываем функцию загрузки данных при загрузке страницы и устанавливаем интервал
    loadDeviceData();
    setInterval(function () {
        loadDeviceData();
    }, 8000);

    // Обработчик событий изменения для выпадающего списка
    $('#deviceDropdown').change(function () {
        currentPageInfo = 1;
        currentPageMeasurements = 1;
        loadDeviceData(currentPageInfo, currentPageMeasurements);
    });

    // Обработчик события клика для переключения вкладок
    $('#dataTabs a').on('shown.bs.tab', function (e) {
        var targetTab = $(e.target).attr('id');
        if (targetTab === 'infoTab') {
            loadDeviceData(currentPageInfo, currentPageMeasurements);
        } else if (targetTab === 'measurementsTab') {
            loadDeviceData(currentPageInfo, currentPageMeasurements);
        }
    });

    // Обработчик события клика для переключения на другую страницу (для информации об устройстве)
    $(document).on('click', '#infoPaginationContainer .page-link', function (e) {
        e.preventDefault();
        var page = $(this).data('page');
        if (page !== currentPageInfo) {
            currentPageInfo = page;
            loadDeviceData(currentPageInfo, currentPageMeasurements);
        }
    });

    // Обработчик события клика для переключения на другую страницу (для измерений устройства)
    $(document).on('click', '#measurementsPaginationContainer .page-link', function (e) {
        e.preventDefault();
        var page = $(this).data('page');
        if (page !== currentPageMeasurements) {
            currentPageMeasurements = page;
            loadDeviceData(currentPageInfo, currentPageMeasurements);
        }
    });

    function loadDeviceData(pageInfo, pageMeasurements) {
        var deviceId = $('#deviceDropdown').val();
        var activeTab = $('#dataTabs .nav-link.active').attr('id');

        var url = '/tables/device_data/';

        var data = {'device_id': deviceId};

        if (activeTab === 'infoTab') {
            url = '/tables/device_data/';
            data['page_info'] = pageInfo;
        } else if (activeTab === 'measurementsTab') {
            url = '/tables/device_data/';
            data['page_measurements'] = pageMeasurements;
        }

        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            success: function (data) {
                if (activeTab === 'infoTab') {
                    updateDeviceInfoTable(data);
                    updateInfoPagination(data);
                } else if (activeTab === 'measurementsTab') {
                    updateDeviceMeasurementsTable(data);
                    updateMeasurementsPagination(data);
                }
            }
        });
    }

    function updateDeviceInfoTable(data) {
        var tableBody = $('#deviceInfoTableBody');
        tableBody.empty();

        if (data.device_info.length === 0) {
            tableBody.append('<tr><td colspan="6">Нет данных для выбранного устройства</td></tr>');
        } else {
            $.each(data.device_info, function (index, info) {
                var insideOrOutside = info.inside_or_not ? 'Inside' : 'Not';
                var row = '<tr>' +
                    '<td>' + info.battery_charge + ' %</td>' +
                    '<td>' + info.satellite_count + ' </td>' +
                    '<td>' + info.latitude + '</td>' +
                    '<td>' + info.longitude + '</td>' +
                    '<td>' + insideOrOutside + '</td>' +
                    '<td>' + info.date_time + '</td>' +
                    '</tr>';
                tableBody.append(row);
            });
        }
    }

    function updateDeviceMeasurementsTable(data) {
        var tableBody = $('#deviceMeasurementsTableBody');
        tableBody.empty();

        if (data.device_measurements.length === 0) {
            tableBody.append('<tr><td colspan="8">Нет данных для выбранного устройства</td></tr>');
        } else {
            $.each(data.device_measurements, function (index, measurement) {
                var row = '<tr>' +
/*                     '<td>' + measurement.measurement_id + '</td>' + */
                    '<td>' + measurement.cumulative_angle + ' °F</td>' +
                    '<td>' + measurement.pressure + ' Pa</td>' +
                    '<td>' + measurement.altitude + ' m</td>' +
                    '<td>' + measurement.temperature + ' °C</td>' +
                    '<td>' + measurement.humidity + ' %</td>' +
                    '<td>' + measurement.taser_activations + '</td>' +
                    '<td>' + measurement.date_time + '</td>' +
                    '</tr>';
                tableBody.append(row);
            });
        }
    }

// Function to update pagination for information
function updateInfoPagination(data) {
    var paginationContainer = $('#infoPaginationContainer');
    paginationContainer.empty();

    var totalPages = data.total_pages_info;
    var currentPage = data.current_page_info;

    var previousPageLink = '<li class="page-item ' + (currentPage === 1 ? 'disabled' : '') + '">' +
        '<a class="page-link" href="#" data-page="' + (currentPage - 1) + '" aria-label="Previous">' +
        '<span aria-hidden="true">&laquo;</span>' +
        '</a>' +
        '</li>';
    paginationContainer.append(previousPageLink);

    var maxDisplayedPages = 15;
    var startPage = Math.max(1, currentPage - Math.floor(maxDisplayedPages / 2));
    var endPage = Math.min(totalPages, startPage + maxDisplayedPages - 1);

    for (var i = startPage; i <= endPage; i++) {
        var pageLink = '<li class="page-item ' + (i === currentPage ? 'active' : '') + '">' +
            '<a class="page-link" href="#" data-page="' + i + '">' + i + '</a>' +
            '</li>';
        paginationContainer.append(pageLink);
    }

    var nextPageLink = '<li class="page-item ' + (currentPage === totalPages ? 'disabled' : '') + '">' +
        '<a class="page-link" href="#" data-page="' + (currentPage + 1) + '" aria-label="Next">' +
        '<span aria-hidden="true">&raquo;</span>' +
        '</a>' +
        '</li>';
    paginationContainer.append(nextPageLink);
}

// Function to update pagination for measurements
function updateMeasurementsPagination(data) {
    var paginationContainer = $('#measurementsPaginationContainer');
    paginationContainer.empty();

    var totalPages = data.total_pages_measurements;
    var currentPage = data.current_page_measurements;

    var previousPageLink = '<li class="page-item ' + (currentPage === 1 ? 'disabled' : '') + '">' +
        '<a class="page-link" href="#" data-page="' + (currentPage - 1) + '" aria-label="Previous">' +
        '<span aria-hidden="true">&laquo;</span>' +
        '</a>' +
        '</li>';
    paginationContainer.append(previousPageLink);

    var maxDisplayedPages = 15;
    var startPage = Math.max(1, currentPage - Math.floor(maxDisplayedPages / 2));
    var endPage = Math.min(totalPages, startPage + maxDisplayedPages - 1);

    for (var i = startPage; i <= endPage; i++) {
        var pageLink = '<li class="page-item ' + (i === currentPage ? 'active' : '') + '">' +
            '<a class="page-link" href="#" data-page="' + i + '">' + i + '</a>' +
            '</li>';
        paginationContainer.append(pageLink);
    }

    var nextPageLink = '<li class="page-item ' + (currentPage === totalPages ? 'disabled' : '') + '">' +
        '<a class="page-link" href="#" data-page="' + (currentPage + 1) + '" aria-label="Next">' +
        '<span aria-hidden="true">&raquo;</span>' +
        '</a>' +
        '</li>';
    paginationContainer.append(nextPageLink);
}


});