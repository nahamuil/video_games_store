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

function logout() {
    // Hide main section
    document.getElementById('main-section').classList.add('hidden');
    // Show login section
    document.getElementById('login-section').classList.remove('hidden');
    // Clear all forms
    clearCustomerForm();
    clearGameForm();
    clearLoanForm();
    // Clear login form
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
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
    // Get all form values
    const title = document.getElementById('game-title').value;
    const publisher = document.getElementById('game-publisher').value;
    const releaseYear = parseInt(document.getElementById('game-year').value);
    const genre = document.getElementById('game-genre').value;
    const price = parseFloat(document.getElementById('game-price').value);
    const quantity = parseInt(document.getElementById('game-quantity').value);
    const imageUrl = document.getElementById('game-image-url').value;

    // Validation checks with specific messages
    if (!title.trim()) {
        alert('Title is required');
        document.getElementById('game-title').focus();
        return;
    }

    if (!publisher.trim()) {
        alert('Publisher is required');
        document.getElementById('game-publisher').focus();
        return;
    }

    if (!releaseYear || isNaN(releaseYear)) {
        alert('Release year must be a valid number');
        document.getElementById('game-year').focus();
        return;
    }

    if (!validateYear(releaseYear)) {
        alert('Release year must be between 1900 and current year');
        document.getElementById('game-year').focus();
        return;
    }

    if (!genre) {
        alert('Please select a genre');
        document.getElementById('game-genre').focus();
        return;
    }

    if (!price || isNaN(price) || price <= 0) {
        alert('Price must be a valid positive number');
        document.getElementById('game-price').focus();
        return;
    }

    if (!quantity || isNaN(quantity) || quantity < 0) {
        alert('Quantity must be a valid non-negative number');
        document.getElementById('game-quantity').focus();
        return;
    }

    if (!imageUrl.trim()) {
        alert('Image URL is required');
        document.getElementById('game-image-url').focus();
        return;
    }

    const data = {
        title,
        publisher,
        release_year: releaseYear,
        genre,
        price,
        quantity,
        image_url: imageUrl
    };

    try {
        await axios.post(`${API_URL}/games`, data);
        loadGames();
        clearGameForm();
        alert('Game added successfully!');
    } catch (error) {
        const errorMessage = error.response?.data?.error || 'Error adding game';
        alert(errorMessage);
    }
}

// Helper function for year validation (unchanged)
function validateYear(year) {
    const currentYear = new Date().getFullYear();
    return year >= 1900 && year <= currentYear;
}

// Loan Management
async function createLoan() {
    const gameId = document.getElementById('loan-game').value;
    const customerId = document.getElementById('loan-customer').value;

    // Validate Loan Form
    if (!gameId || !customerId) {
        alert('Please select a game and a customer.');
        return;
    }

    const data = {game_id: gameId, customer_id: customerId};

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
    document.getElementById('game-image-url').value = '';  // Added clearing image URL
}

function clearLoanForm() {
    document.getElementById('loan-customer').value = '';
    document.getElementById('loan-game').value = '';
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
        // Add to games list
        gamesList.innerHTML += createGameCard(game);

        // Add to loan selection dropdown if quantity > 0
        if (game.quantity > 0) {
            select.innerHTML += `<option value="${game.id}">${game.title}</option>`;
        }
    });
}

async function deleteGame(gameId) {
    if (!confirm('Are you sure you want to delete this game? This action cannot be undone.')) {
        return;
    }

    try {
        await axios.delete(`${API_URL}/games/${gameId}`);
        loadGames(); // Reload the games list
    } catch (error) {
        const errorMessage = error.response?.data?.error || 'Error deleting game';
        alert(errorMessage);
    }
}

// Update the createGameCard function to include a delete button
function createGameCard(game) {
    return `
        <div class="game-card">
            <img src="${game.image_url}" alt="${game.title}" class="w-full h-48 object-cover mb-2">
            <h3 class="font-bold">${game.title}</h3>
            <p>Publisher: ${game.publisher}</p>
            <p>Year: ${game.release_year}</p>
            <p>Genre: ${game.genre}</p>
            <p>Price: $${game.price}</p>
            <p>Available: ${game.quantity}</p>
            <button onclick="deleteGame(${game.id})" class="danger">Delete Game</button>
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
    try {
        const response = await axios.get(`${API_URL}/loans`);
        const loansList = document.getElementById('active-loans');
        loansList.innerHTML = '';

        if (response.data && Array.isArray(response.data)) {
            response.data.forEach(loan => {
                loansList.innerHTML += createLoanCard(loan);
            });
        }
    } catch (error) {
        console.error('Error loading loans:', error);
        alert('Error loading loans');
    }
}

function createLoanCard(loan) {
    // Add null checks to prevent undefined errors
    if (!loan || !loan.game || !loan.customer) {
        console.error('Invalid loan data:', loan);
        return '';
    }

    return `
        <div class="loan-card">
            <h3 class="font-bold">${loan.game.title}</h3>
            <p>Customer: ${loan.customer.name}</p>
            <p>Loaned On: ${loan.loan_date}</p>
            <p>Price: $${loan.price.toFixed(2)}</p>
            <button onclick="returnLoan(${loan.id})" class="danger">Return</button>
        </div>
    `;
}


async function returnLoan(loanId) {
    try {
        const response = await axios.post(`${API_URL}/loans/${loanId}/return`);
        if (response.status === 200) {
            await loadLoans();  // Refresh the loans list
            await loadGames();  // Refresh the games list to update quantities
            alert('Game returned successfully!');
        }
    } catch (error) {
        console.error('Error returning loan:', error);
        const errorMessage = error.response?.data?.error || 'Error returning loan';
        alert(errorMessage);
    }
}

