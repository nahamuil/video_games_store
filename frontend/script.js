// script.js
const API_URL = 'http://localhost:5000/api';

// Authentication
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post(`${API_URL}/login`, {username, password});
        if (response.data.success) {
            document.getElementById('login-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
            loadDashboard();
        }
    } catch (error) {
        const errorMessage = error.response?.data?.message || 'An error occurred';

        if (errorMessage === 'Incorrect password') {
            alert('Wrong password for this username. Please try again.');
        } else if (errorMessage === 'Invalid username') {
            alert('Username not found. Please check your credentials.');
        } else {
            alert('Login failed. Please try again.');
        }
    }
}

// Customer Management
async function addCustomer() {
    const data = {
        name: document.getElementById('customer-name').value,
        email: document.getElementById('customer-email').value,
        phone: document.getElementById('customer-phone').value
    };

    try {
        await axios.post(`${API_URL}/customers`, data);
        loadCustomers();
        clearCustomerForm();
    } catch (error) {
        alert('Error adding customer');
    }
}

async function loadCustomers() {
    const response = await axios.get(`${API_URL}/customers`);
    const select = document.getElementById('loan-customer');
    select.innerHTML = '<option value="">Select Customer</option>';
    response.data.forEach(customer => {
        select.innerHTML += `<option value="${customer.id}">${customer.name}</option>`;
    });
}

// Game Management
async function addGame() {
    const data = {
        title: document.getElementById('game-title').value,
        publisher: document.getElementById('game-publisher').value,
        release_year: parseInt(document.getElementById('game-year').value),
        genre: document.getElementById('game-genre').value,
        price: parseFloat(document.getElementById('game-price').value),
        quantity: parseInt(document.getElementById('game-quantity').value)
    };

    try {
        await axios.post(`${API_URL}/games`, data);
        loadGames();
        clearGameForm();
    } catch (error) {
        alert('Error adding game');
    }
}

async function loadGames() {
    const response = await axios.get(`${API_URL}/games`);
    const gamesList = document.getElementById('games-list');
    const select = document.getElementById('loan-game');

    gamesList.innerHTML = '';
    select.innerHTML = '<option value="">Select Game</option>';

    response.data.forEach(game => {
        gamesList.innerHTML += createGameCard(game);
        if (game.available) {
            select.innerHTML += `<option value="${game.id}">${game.title}</option>`;
        }
    });
}

// Loan Management
async function createLoan() {
    const data = {
        game_id: document.getElementById('loan-game').value,
        customer_id: document.getElementById('loan-customer').value,
        price: parseFloat(document.getElementById('loan-price').value)
    };

    try {
        await axios.post(`${API_URL}/loans`, data);
        loadLoans();
        loadGames();
        clearLoanForm();
    } catch (error) {
        alert('Error creating loan');
    }
}

async function loadLoans() {
    const response = await axios.get(`${API_URL}/loans`);
    const loansList = document.getElementById('active-loans');
    loansList.innerHTML = '';

    response.data.forEach(loan => {
        loansList.innerHTML += createLoanCard(loan);
    });
}

async function returnLoan(loanId) {
    try {
        await axios.post(`${API_URL}/loans/${loanId}/return`);
        loadLoans();
        loadGames();
    } catch (error) {
        alert('Error returning loan');
    }
}

// Helper Functions
function createGameCard(game) {
    return `
        <div class="bg-white p-4 rounded-lg shadow">
            <h3 class="font-bold">${game.title}</h3>
            <p>Publisher: ${game.publisher}</p>
            <p>Year: ${game.release_year}</p>
            <p>Genre: ${game.genre}</p>
            <p>Price: $${game.price}</p>
            <p>Available: ${game.quantity}</p>
        </div>
    `;
}

function createLoanCard(loan) {
    return `
        <div class="bg-white p-4 rounded-lg shadow">
            <h3 class="font-bold">${loan.game_title}</h3>
            <p>Customer: ${loan.customer_name}</p>
            <p>Loan Date: ${new Date(loan.loan_date).toLocaleDateString()}</p>
            <p>Price: $${loan.price}</p>
            <button onclick="returnLoan(${loan.id})" class="bg-blue-500 text-white px-4 py-2 rounded">
                Return
            </button>
        </div>
    `;
}

function loadDashboard() {
    loadCustomers();
    loadGames();
    loadLoans();
}

function clearCustomerForm() {
    ['customer-name', 'customer-email', 'customer-phone'].forEach(id => {
        document.getElementById(id).value = '';
    });
}

function clearGameForm() {
    ['game-title', 'game-publisher', 'game-year', 'game-genre', 'game-price', 'game-quantity'].forEach(id => {
        document.getElementById(id).value = '';
    });
}

function clearLoanForm() {
    ['loan-game', 'loan-customer', 'loan-price'].forEach(id => {
        document.getElementById(id).value = '';
    });
}