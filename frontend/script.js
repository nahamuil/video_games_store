// API URL
const API_URL = 'http://127.0.0.1:5000';

// Authentication Functions
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post(`${API_URL}/login`, {
            username: username,
            password: password
        });

        localStorage.setItem('token', response.data.token);
        showMainSection();
        await loadGames();
    } catch (error) {
        alert('Login failed: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post(`${API_URL}/register`, {
            username: username,
            password: password
        });
        alert('Registration successful! Please login.');
    } catch (error) {
        alert('Registration failed: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

function logout() {
    localStorage.removeItem('token');
    showAuthSection();
}

// UI Helper Functions
function showMainSection() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-section').classList.remove('hidden');
}

function showAuthSection() {
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('main-section').classList.add('hidden');
}

// Game Management Functions
async function loadGames() {
    try {
        const response = await axios.get(`${API_URL}/games`, {
            headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
        });

        const gamesList = document.getElementById('games-list');
        const loanedGamesList = document.getElementById('loaned-games-list');

        gamesList.innerHTML = '';
        loanedGamesList.innerHTML = '';

        response.data.games.forEach(game => {
            const gameCard = createGameCard(game);
            if (game.is_loaned) {
                loanedGamesList.appendChild(gameCard);
            } else {
                gamesList.appendChild(gameCard);
            }
        });
    } catch (error) {
        alert('Error loading games: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

function createGameCard(game) {
    const div = document.createElement('div');
    div.className = 'bg-gray-50 p-4 rounded-lg shadow';
    div.innerHTML = `
        <h3 class="font-bold text-lg">${game.title}</h3>
        <p class="text-gray-600">Creator: ${game.creator}</p>
        <p class="text-gray-600">Year: ${game.year_published}</p>
        <p class="text-gray-600">Genre: ${game.genre}</p>
        <p class="text-gray-600">Price: $${game.price}</p>
        <p class="text-gray-600">Quantity: ${game.quantity}</p>
        <div class="mt-4 flex justify-between">
            ${!game.is_loaned ?
        `<button onclick="loanGame(${game.id})" class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
                    Loan Game
                </button>` :
        `<button onclick="returnGame(${game.id})" class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600">
                    Return Game
                </button>`
    }
            <button onclick="deleteGame(${game.id})" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
                Delete
            </button>
        </div>
    `;
    return div;
}

async function addGame() {
    const title = document.getElementById('game-title').value;
    const creator = document.getElementById('game-creator').value;
    const year = document.getElementById('game-year').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post(`${API_URL}/games`, {
            title: title,
            creator: creator,
            year_published: parseInt(year),
            genre: genre,
            price: parseFloat(price),
            quantity: parseInt(quantity)
        }, {
            headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
        });

        // Clear form
        document.getElementById('game-title').value = '';
        document.getElementById('game-creator').value = '';
        document.getElementById('game-year').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        await loadGames();
        alert('Game added successfully!');
    } catch (error) {
        alert('Error adding game: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

async function deleteGame(gameId) {
    if (!confirm('Are you sure you want to delete this game?')) return;

    try {
        await axios.delete(`${API_URL}/games/${gameId}`, {
            headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
        });
        await loadGames();
        alert('Game deleted successfully!');
    } catch (error) {
        alert('Error deleting game: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

async function loanGame(gameId) {
    try {
        await axios.post(`${API_URL}/games/${gameId}/loan`, {}, {
            headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
        });
        await loadGames();
        alert('Game loaned successfully!');
    } catch (error) {
        alert('Error loaning game: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

async function returnGame(gameId) {
    try {
        await axios.post(`${API_URL}/games/${gameId}/return`, {}, {
            headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
        });
        await loadGames();
        alert('Game returned successfully!');
    } catch (error) {
        alert('Error returning game: ' + (error.response?.data?.message || 'Unknown error'));
    }
}

// Check authentication status on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        showMainSection();
        loadGames();
    } else {
        showAuthSection();
    }
});