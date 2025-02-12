from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Load the Excel file containing game data
games_data = pd.read_excel('games_list.xlsx')

# Set up the ChromeDriver service
service = Service(executable_path='path_to_chromedriver')

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=service)

# Open your site
driver.get("http://localhost:63342/video_games_store/frontend")

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Loop through each game in the Excel file and add it to the site
for index, game in games_data.iterrows():
    # Click on the "Add Game" button or navigate to the form
    add_game_button = wait.until(EC.element_to_be_clickable((By.ID, 'add-game-btn')))
    add_game_button.click()

    # Wait for the form to be visible
    title_input = wait.until(EC.visibility_of_element_located((By.ID, 'game-title')))
    publisher_input = driver.find_element(By.ID, 'game-publisher')
    release_year_input = driver.find_element(By.ID, 'game-release-year')
    genre_input = driver.find_element(By.ID, 'game-genre')
    price_input = driver.find_element(By.ID, 'game-price')
    quantity_input = driver.find_element(By.ID, 'game-quantity')
    image_url_input = driver.find_element(By.ID, 'game-image-url')

    # Fill in the game data
    title_input.clear()
    title_input.send_keys(game['Title'])
    publisher_input.clear()
    publisher_input.send_keys(game['Publisher'])
    release_year_input.clear()
    release_year_input.send_keys(str(game['Release Year']))
    genre_input.clear()
    genre_input.send_keys(game['Genre'])
    price_input.clear()
    price_input.send_keys(str(game['Price']))
    quantity_input.clear()
    quantity_input.send_keys(str(game['Quantity']))
    image_url_input.clear()
    image_url_input.send_keys(game['Image URL'])

    # Submit the form
    submit_button = driver.find_element(By.ID, 'submit-game-btn')
    submit_button.click()

    # Wait a moment before adding the next game
    time.sleep(2)

# Close the browser after all games have been added
driver.quit()
