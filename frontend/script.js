async function getVideoGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/video_games');
        const videoGamesList = document.getElementById('video-games-list');
        videoGamesList.innerHTML = ''; // Clear existing list

        response.data.video_games.forEach(video_game => {
            videoGamesList.innerHTML += `
                <div class="video-game-card">
                    <h3>${video_game.title}</h3>
                    <p>Author: ${video_game.author}</p>
                    <p>Year: ${video_game.year_published}</p>
                    <p>Type: ${video_game.type}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching books:', error);
        alert('Failed to load books');
    }
}

// function to add a new book to the database
async function addBook() {
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const year_published = document.getElementById('book-year-published').value;
    const types = document.getElementById('book-type').value;

    try {
        await axios.post('http://127.0.0.1:5000/books', {
            title: title,
            author: author,
            year_published: year_published,
            types: types
        });

        // Clear form fields
        document.getElementById('book-title').value = '';
        document.getElementById('book-author').value = '';
        document.getElementById('book-year-published').value = '';
        document.getElementById('book-type').value = '';

        // Refresh the books list
        getBooks();

        alert('Book added successfully!');
    } catch (error) {
        console.error('Error adding book:', error);
        alert('Failed to add book');
    }
}

// Load all books when page loads
document.addEventListener('DOMContentLoaded', getBooks);