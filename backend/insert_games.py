import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    chrome_options = Options()
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)


def interact_with_form():
    driver = setup_driver()

    try:
        driver.get(r"C:\user\ofek\PycharmProjects\PythonProject\video_games_store\frontend\index.html")

        wait = WebDriverWait(driver, 10)

        # Select English language
        username_field = wait.until(EC.presence_of_element_located((By.ID, "Username")))
        username_field.send_keys("o")

        password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys("123")

        wait = WebDriverWait(driver, 1000)

        # Wait for game to load
        wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))

        # Enhanced JavaScript clicking implementation with multiple optimizations
        driver.execute_script("""
            // Store references to avoid repeated DOM lookups
            const bigCookie = document.getElementById('bigCookie');
            const shimmer = document.getElementById('shimmers');
            const upgrades = document.getElementById('upgrades');
            const products = document.getElementById('products');

            // Optimization: Use performance.now() for more precise timing
            let lastUpdate = performance.now();
            const UPDATE_INTERVAL = 100; // Check upgrades every 100ms

            // Click golden cookies when they appear
            const clickGolden = () => {
                if (shimmer && shimmer.firstChild) {
                    shimmer.firstChild.click();
                }
            };

            // Buy available upgrades
            const buyUpgrades = () => {
                if (upgrades) {
                    const upgrade = upgrades.querySelector('.upgrade.enabled');
                    if (upgrade) upgrade.click();
                }
            };

            // Buy available products (buildings)
            const buyProducts = () => {
                if (products) {
                    const buildings = Array.from(products.children).reverse();
                    for (let building of buildings) {
                        if (building.classList.contains('enabled')) {
                            building.click();
                            break;
                        }
                    }
                }
            };

            // Main game loop using requestAnimationFrame for optimal performance
            const gameLoop = () => {
                // Click cookie as fast as possible
                bigCookie.click();

                // Check for upgrades and buildings periodically
                const now = performance.now();
                if (now - lastUpdate > UPDATE_INTERVAL) {
                    clickGolden();
                    buyUpgrades();
                    buyProducts();
                    lastUpdate = now;
                }

                requestAnimationFrame(gameLoop);
            };

            // Start the game loop
            requestAnimationFrame(gameLoop);

            // Expose control variable to stop the loop
            window.isRunning = true;
        """)

        # Monitor progress with enhanced efficiency
        cookies_field = driver.find_element(By.ID, "cookies")
        target = 10000

        while get_cookies_amount(cookies_field.text) < target:
            time.sleep(0.1)

        # Stop the automation
        driver.execute_script("window.isRunning = false;")

        print(f"Target of {target} cookies reached!")
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    interact_with_form()
