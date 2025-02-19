from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Constants
FRONTEND_URL = r"C:\user\ofek\PyCharm\PyCharmProjects\Ort_PyCharm\video_games_store\frontend\index.html"
DEFAULT_WAIT_TIMEOUT = 15
STEAM_API_URL = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"

# Form field IDs mapping
FORM_FIELDS = {
    'game-title': 'name',
    'game-publisher': 'publisher',
    'game-year': 'release_year',
    'game-genre': 'genre',
    'game-price': 'price',
    'game-quantity': 'quantity',
    'game-image-url': 'header_image'
}

# Dropdown mapping to handle mismatched genre values
DROPDOWN_GENRE_MAPPING = {
    'Action-Adventure': 'Action',
    'RPG (Role-Playing Game)': 'RPG',
    'First-Person Shooter': 'Shooter',
    'Sandbox': 'Simulation',
    'Adventure': 'Action',
    'Strategy': 'RPG',
    'Racing': 'Sports',
    'Sports': 'Sports',
    'Simulation': 'Simulation',
    'Casual': 'Casual'
}

# Setting up the Chrome WebDriver
chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)

# Dropdown options caching
dropdown_options_cache = None


def get_steam_game_details(app_id):
    """Fetch detailed information about a specific game from Steam."""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data[str(app_id)]['success']:
                game_data = data[str(app_id)]['data']

                # Extract and format the price
                price = "29.99"  # Default price
                if 'price_overview' in game_data:
                    price = str(game_data['price_overview'].get('final', 2999) / 100)

                # Extract and format the genre
                genre = 'Action'  # Default genre
                if 'genres' in game_data and len(game_data['genres']) > 0:
                    genre = game_data['genres'][0]['description']

                # Extract year from release date
                year = '2024'  # Default year
                if 'release_date' in game_data and 'date' in game_data['release_date']:
                    date_str = game_data['release_date']['date']
                    if date_str and len(date_str) >= 4:
                        year = date_str[-4:]

                return {
                    'name': game_data.get('name', ''),
                    'publisher': game_data.get('publishers', ['Unknown Publisher'])[0],
                    'release_year': year,
                    'genre': genre,
                    'price': price,
                    'quantity': '10',  # Default quantity
                    'header_image': game_data.get('header_image', '')
                }
    except Exception as e:
        print(f"Error fetching details for app {app_id}: {e}")
    return None


def get_steam_games(limit=10):
    """Fetch popular games from Steam."""
    games_list = []
    try:
        response = requests.get(STEAM_API_URL)
        if response.status_code == 200:
            data = response.json()
            games = data['response'].get('ranks', [])

            for game in games[:limit]:
                app_id = game['appid']
                game_details = get_steam_game_details(app_id)
                if game_details:
                    games_list.append(game_details)
                time.sleep(1)  # Prevent rate limiting
    except Exception as e:
        print(f"Error fetching Steam games: {e}")
    return games_list


def initialize_frontend(url):
    """Navigate to the frontend page."""
    print("Initializing frontend...")
    driver.get(url)


def login_to_site(username, password):
    """Perform login on the site."""
    print("Logging in...")
    username_field = wait.until(EC.visibility_of_element_located((By.ID, 'username')))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'password')))
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))

    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    login_button.click()

    wait.until(EC.visibility_of_element_located((By.ID, 'main-section')))
    print("Login successful.")


def get_dropdown_options(field_id):
    """Retrieve all available dropdown options and cache them."""
    global dropdown_options_cache
    if dropdown_options_cache is None:
        dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID, field_id))))
        dropdown_options_cache = [option.get_attribute('value') for option in dropdown.options if option.get_attribute('value')]
        print(f"Cached dropdown options for '{field_id}': {dropdown_options_cache}")
    return dropdown_options_cache


def scroll_into_view(element):
    """Scroll the page to bring an element into view."""
    driver.execute_script("arguments[0].scrollIntoView();", element)


def fill_form_field(field_id, value):
    """Fill a form field or select a value in a dropdown."""
    print(f"Filling field '{field_id}' with value: {value}")

    # Scroll the element into view
    element = driver.find_element(By.ID, field_id)
    scroll_into_view(element)

    if field_id == 'game-genre':  # Handle dropdown fields
        options = get_dropdown_options(field_id)

        # Map invalid dropdown values to valid ones
        if value in DROPDOWN_GENRE_MAPPING:
            value = DROPDOWN_GENRE_MAPPING[value]
            print(f"Mapped genre value: '{value}'")

        if value not in options:
            print(f"Warning: Genre '{value}' not found in dropdown. Using default 'Action'")
            value = 'Action'

        dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID, field_id))))
        dropdown.select_by_value(value)
    else:  # Handle text input fields
        input_field = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
        input_field.clear()
        input_field.send_keys(str(value))


def handle_alert():
    """Handle alerts after form submission."""
    try:
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.accept()
    except Exception as e:
        print(f"No alert detected. Error: {e}")


def submit_form():
    """Submit the form and handle alerts."""
    submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'success') and text()='Add Game']")
    scroll_into_view(submit_button)  # Ensure the button is in view
    submit_button.click()
    handle_alert()


def add_game_to_site(game_data):
    """Fill form fields with game data and submit the form."""
    print(f"Adding game: {game_data['name']}...")
    try:
        for field_id, column_name in FORM_FIELDS.items():
            value = game_data[column_name]
            fill_form_field(field_id, str(value).strip())

        submit_form()
        print(f"Game '{game_data['name']}' added successfully.")
    except Exception as e:
        print(f"Error while adding game '{game_data['name']}': {e}")


# Main execution
try:
    # Initialize the site
    initialize_frontend(FRONTEND_URL)

    # Log in
    login_to_site(username='o', password='123')

    # Fetch and process games from Steam
    print("Fetching games from Steam...")
    steam_games = get_steam_games(limit=10)  # Fetch 10 games
    print(f"Found {len(steam_games)} games to process")

    # Process each game
    for index, game_data in enumerate(steam_games):
        print(f"Processing game {index + 1}/{len(steam_games)}...")
        add_game_to_site(game_data)
        time.sleep(2)  # Add delay between submissions
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Closing the browser...")
    driver.quit()