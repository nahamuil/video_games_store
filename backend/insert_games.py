from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Constants
GAMES_FILE = 'games_list.xlsx'  # Path to the Excel file
FRONTEND_URL = r"C:\user\ofek\PyCharm\PyCharmProjects\Ort_PyCharm\video_games_store\frontend\index.html"
DEFAULT_WAIT_TIMEOUT = 15

# Form field IDs and Excel column mapping
FORM_FIELDS = {
    'game-title': 'Title',
    'game-publisher': 'Publisher',
    'game-year': 'Release Year',
    'game-genre': 'Genre',
    'game-price': 'Price',
    'game-quantity': 'Quantity',
    'game-image-url': 'Image URL'
}

# Dropdown mapping to handle mismatched genre values
DROPDOWN_GENRE_MAPPING = {
    'Action-Adventure': 'Action',
    'RPG (Role-Playing Game)': 'RPG',
    'First-Person Shooter': 'Shooter',
    'Sandbox': 'Simulation'  # Map 'Sandbox' to 'Simulation'
}

# Load game data from the Excel file
games_df = pd.read_excel(GAMES_FILE)

# Setting up the Chrome WebDriver
chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)

# Dropdown options caching
dropdown_options_cache = None


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
            raise Exception(
                f"Option '{value}' not found in dropdown '{field_id}'. Available options are: {options}"
            )

        dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID, field_id))))
        dropdown.select_by_value(value)
    else:  # Handle text input fields
        input_field = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
        input_field.clear()
        input_field.send_keys(value)


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
    print(f"Adding game: {game_data['Title']}...")
    try:
        for field_id, column_name in FORM_FIELDS.items():
            value = game_data[column_name]
            fill_form_field(field_id, str(value).strip())

        submit_form()
        print(f"Game '{game_data['Title']}' added successfully.")
    except Exception as e:
        print(f"Error while adding game '{game_data['Title']}': {e}")


# Main execution
try:
    # Initialize the site
    initialize_frontend(FRONTEND_URL)

    # Log in
    login_to_site(username='o', password='123')

    # Process games from the Excel file
    for index, game_data in games_df.iterrows():
        print(f"Processing game {index + 1}/{len(games_df)}...")
        add_game_to_site(game_data)
finally:
    print("Closing the browser...")
    driver.quit()
