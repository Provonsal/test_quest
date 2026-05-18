// Сохранение токенов
function saveTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
}

// Получение токенов
function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

// Удаление токенов (выход)
function removeTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/user/login';
}

// Проверка аутентификации
function isAuthenticated() {
    return !!getAccessToken();
}

// Обновление access токена
async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    
    if (!refreshToken) {
        removeTokens();
        return null;
    }
    
    try {
        const response = await fetch('/api/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh_token: refreshToken })
        });
        
        if (response.ok) {
            const data = await response.json();
            saveTokens(data.access_token, data.refresh_token);
            return data.access_token;
        } else {
            removeTokens();
            return null;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
        removeTokens();
        return null;
    }
}

// Универсальная функция для API запросов с JWT
async function authFetch(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });
        
        // Если получаем редирект
        if (response.redirected) {
            window.location.href = response.url;
            return null;
        }
        
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('text/html')) {
            const html = await response.text();
            
            // Обновляем страницу
            updatePageContent(html, response.url);
            
            return null;
        }
        
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        return response;
        
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}

function updatePageContent(html, newUrl) {
    // Сохраняем состояние перед обновлением
    const currentState = {
        html: document.documentElement.outerHTML,
        url: window.location.href,
        title: document.title
    };
    
    // Парсим новый HTML
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    
    // Обновляем содержимое
    document.body.innerHTML = doc.body.innerHTML;
    document.title = doc.title;
    
    // Обновляем URL
    if (newUrl) {
        window.history.pushState(currentState, '', newUrl);
    }
    
    // Обработка кнопки "назад" в браузере
    window.addEventListener('popstate', function(event) {
        if (event.state && event.state.html) {
            const parser = new DOMParser();
            const oldDoc = parser.parseFromString(event.state.html, 'text/html');
            document.body.innerHTML = oldDoc.body.innerHTML;
            document.title = event.state.title;
        }
    });
}

// Обновленная функция входа
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        // Используем form-data для OAuth2 совместимости
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            saveTokens(data.access_token, data.refresh_token);
            showMessage('Вход выполнен успешно!', 'success');
            
            // Загружаем защищенную страницу
            setTimeout(async () => {
                let response = await authFetch('/user/profile');
                if (response.ok){
                    window.document = response;
                }
            }, 500);
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Ошибка входа', 'error-message');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error-message');
    }
}

// Загрузка данных пользователя
async function loadUserProfile() {
    try {
        const response = await authFetch('/user/profile');
        
        if (response.ok) {
            const user = await response.json();
            console.log('User data:', user);
            // Отображаем данные пользователя на странице
            document.getElementById('userName').textContent = user.full_name;
            document.getElementById('userEmail').textContent = user.email;
        }
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

// Проверка аутентификации при загрузке защищенных страниц
document.addEventListener('DOMContentLoaded', function() {
    // Если мы на защищенной странице
    if (window.location.pathname === '/user/profile') {
        if (!isAuthenticated()) {
            window.location.href = '/';
        } else {
            loadUserProfile();
        }
    }
});