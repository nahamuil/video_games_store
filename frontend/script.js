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
        alert(errorMessage);
    }
}

// Customer Management
async function addCustomer() {
    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('customer-email').value;
    const phone = document.getElementById('customer-phone').value;

    // Validate Customer Form
    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (!validatePhoneNumber(phone)) {
        alert('Please enter a valid phone number (10 digits).');
        return;
    }

    const data = {name, email, phone};

    try {
        await axios.post(`${API_URL}/customers`, data);
        loadCustomers();
        clearCustomerForm();
    } catch (error) {
        alert('Error adding customer');
    }
}

function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

function validatePhoneNumber(phone) {
    const phoneRegex = /^[0-9]{10}$/; // Ensures the phone number is exactly 10 digits
    return phoneRegex.test(phone);
}

// Game Management
async function addGame() {
    const title = document.getElementById('game-title').value;
    const publisher = document.getElementById('game-publisher').value;
    const releaseYear = parseInt(document.getElementById('game-year').value);
    const genre = document.getElementById('game-genre').value;
    const price = parseFloat(document.getElementById('game-price').value);
    const quantity = parseInt(document.getElementById('game-quantity').value);

    // Validate Game Form
    if (!validateYear(releaseYear)) {
        alert('Please enter a valid publish year (between 1900 and current year).');
        return;
    }

    if (!title || !publisher || !genre || !price || !quantity) {
        alert('Please fill all the fields.');
        return;
    }

    const data = {title, publisher, release_year: releaseYear, genre, price, quantity};

    try {
        await axios.post(`${API_URL}/games`, data);
        loadGames();
        clearGameForm();
    } catch (error) {
        alert('Error adding game');
    }
}

function validateYear(year) {
    const currentYear = new Date().getFullYear();
    return year >= 1900 && year <= currentYear;
}

// Loan Management
async function createLoan() {
    const gameId = document.getElementById('loan-game').value;
    const customerId = document.getElementById('loan-customer').value;
    const price = parseFloat(document.getElementById('loan-price').value);
    alert('a.');

    // Validate Loan Form
    if (!gameId || !customerId || !price) {
        alert('Please select a game, customer, and enter the loan price.');
        return;
    }

    alert('b.');

    const data = {game_id: gameId, customer_id: customerId, price};

    try {
        await axios.post(`${API_URL}/loans`, data);
        loadLoans();
        loadGames();
        clearLoanForm();
    } catch (error) {
        alert('Error creating loan');
    }
}

// Helper Functions
function clearCustomerForm() {
    document.getElementById('customer-name').value = '';
    document.getElementById('customer-email').value = '';
    document.getElementById('customer-phone').value = '';
}

function clearGameForm() {
    document.getElementById('game-title').value = '';
    document.getElementById('game-publisher').value = '';
    document.getElementById('game-year').value = '';
    document.getElementById('game-genre').value = '';
    document.getElementById('game-price').value = '';
    document.getElementById('game-quantity').value = '';
}

function clearLoanForm() {
    document.getElementById('loan-customer').value = '';
    document.getElementById('loan-game').value = '';
    document.getElementById('loan-price').value = '';
}

function loadDashboard() {
    loadGames();
    loadCustomers();
    loadLoans();
}

// Load Games
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

// Load Customers
async function loadCustomers() {
    const response = await axios.get(`${API_URL}/customers`);
    const select = document.getElementById('loan-customer');
    select.innerHTML = '<option value="">Select Customer</option>';
    response.data.forEach(customer => {
        select.innerHTML += `<option value="${customer.id}">${customer.name}</option>`;
    });
}

// Load Loans
async function loadLoans() {
    const response = await axios.get(`${API_URL}/loans`);
    const loansList = document.getElementById('active-loans');
    loansList.innerHTML = '';

    response.data.forEach(loan => {
        loansList.innerHTML += createLoanCard(loan);
    });
}

function createLoanCard(loan) {
    return `
        <div class="bg-white p-4 rounded-lg shadow">
            <h3 class="font-bold">${loan.game.title}</h3>
            <p>Customer: ${loan.customer.name}</p>
            <p>Price: $${loan.price}</p>
            <p>Loaned On: ${loan.loan_date}</p>
            <button onclick="returnLoan(${loan.id})" class="bg-red-500 text-white p-2 rounded">Return</button>
        </div>
    `;
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
