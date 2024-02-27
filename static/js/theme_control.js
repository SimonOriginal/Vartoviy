// Управление темой интерфейса
const body = document.body;
const navbar = document.querySelector('.navbar');

const lightThemeButton = document.getElementById('lightTheme');
const darkThemeButton = document.getElementById('darkTheme');

function applyTheme(theme) {
    var body = document.body;
    var navbar = document.querySelector('.navbar');

    var lightTheme = theme === 'light';

    body.classList.remove(lightTheme ? 'bg-dark' : 'bg-light', lightTheme ? 'text-light' : 'text-dark');
    body.classList.add(lightTheme ? 'bg-light' : 'bg-dark', lightTheme ? 'text-dark' : 'text-light');
    
    navbar.classList.remove(lightTheme ? 'bg-dark' : 'bg-light', 'navbar-' + (lightTheme ? 'dark' : 'light'));
    navbar.classList.add(lightTheme ? 'bg-light' : 'bg-dark', 'navbar-' + (lightTheme ? 'light' : 'dark'));

    var elementsToApplyTheme = document.querySelectorAll('.card-body, .modal-content, .modal-body, .card-header, .dropdown-menu, .dropdown-item, .form-control, .table, .list-group-item, .notification-container, .list-group');

    elementsToApplyTheme.forEach(function(element) {
        element.classList.remove(lightTheme ? 'bg-dark' : 'bg-light', lightTheme ? 'text-light' : 'text-dark');
        element.classList.add(lightTheme ? 'bg-light' : 'bg-dark', lightTheme ? 'text-dark' : 'text-light');
        if (element.classList.contains('plotly-graph-div')) {
            element.style.backgroundColor = lightTheme ? '#FFFFFF' : '#333333';
        }
    });

    localStorage.setItem('theme', theme);
}

function setLightTheme() {
    applyTheme('light');
}

function setDarkTheme() {
    applyTheme('dark');
}

// Функция для проверки сохраненной темы в localStorage
function checkTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        setDarkTheme();
    } else {
        setLightTheme();
    }
}

// Вызываем функцию проверки темы при загрузке страницы
checkTheme();

lightThemeButton.addEventListener('click', setLightTheme);
darkThemeButton.addEventListener('click', setDarkTheme);