from __future__ import annotations  # Allows using class names in type hints before they are defined

import time  # Import time module for sleep function
import random  # Import random module for generating random strings

from ...typing import CreateResult, Messages  # Import custom types
from ..base_provider import AbstractProvider  # Import base provider class
from ..helper import format_prompt, get_random_string  # Import helper functions
from ...webdriver import WebDriver, WebDriverSession  # Import WebDriver and WebDriverSession classes
from ... import debug  # Import debug module

class AItianhuSpace(AbstractProvider):  # Define AItianhuSpace class that inherits from AbstractProvider
    url = "https://chat3.aiyunos.top/"  # URL for the AI Tian Hu chat service
    working = True  # Flag indicating if the provider is working
    supports_stream = True  # Flag indicating if the provider supports streaming responses
    supports_gpt_35_turbo = True  # Flag indicating if the provider supports GPT-3.5-turbo model
    _domains = ["aitianhu.com", "aitianhu1.top"]  # List of allowed domains for AI Tian Hu

    @classmethod
    def create_completion(
            cls,
            model: str,
            messages: Messages,
            stream: bool,
            domain: str = None,
            proxy: str = None,
            timeout: int = 120,
            webdriver: WebDriver = None,
            headless: bool = True,
            **kwargs
    ) -> CreateResult:  # Define create_completion class method that takes required and optional arguments
        # Set the default model to gpt-3.5-turbo if not provided
        if not model:
            model = "gpt-3.5-turbo"

        # Generate a random domain if not provided
        if not domain:
            rand = get_random_string(6)
            domain = random.choice(cls._domains)
            domain = f"{rand}.{domain}"

        # Log the domain used for debugging purposes
        if debug.logging:
            print(f"AItianhuSpace | using domain: {domain}")

        # Construct the URL with the generated domain
        url = f"https://{domain}"

        # Format the prompt using the provided messages
        prompt = format_prompt(messages)

        # Create a WebDriverSession with the provided webdriver, proxy, and headless options
        with WebDriverSession(webdriver, "", headless=headless, proxy=proxy) as driver:
            # Import required Selenium elements
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # Create a WebDriverWait object with the provided timeout
            wait = WebDriverWait(driver, timeout)

            # Bypass devtools detection
            driver.get("https://blank.page/")
            wait.until(EC.visibility_of_element_located((By.ID, "sheet")))
            driver.execute_script(f"""
    document.getElementById('sheet').addEventListener('click', () => {{
        window.open('{url}', '_blank');
    }});
    """)
            driver.find_element(By.ID, "sheet").click()
            time.sleep(10)

            # Switch to the new window with the chat service
            original_window = driver.current_window_handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.close()
                    driver.switch_to.window(window_handle)
                    break

            # Wait for the page to load
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.n-input__textarea-el")))

            # Register a hook in XMLHttpRequest to capture responses
            script = """
const _http_request_open = XMLHttpRequest.prototype.open;
window._last_message = window._message = "";
window._loadend = false;
XMLHttpRequest.prototype.open = function(method, url) {
    if (url == "/api/chat-process") {
        this.addEventListener("progress", (event) => {
            const lines = this.responseText.split("\\n");
            try {
                window._message = JSON.parse(lines[lines.length-1])["text"];
            } catch(e) { }
        });
        this.addEventListener("loadend", (event) => {
            window._loadend = true;
        });
    }
    return _http_request_open.call(this, method, url);
}
"""
            driver.execute_script(script)

            # Submit the prompt
            driver.find_element(By.CSS_SELECTOR, "textarea.n-input__textarea-el").send_keys(prompt)
            driver.find_element(By.CSS_SELECTOR, "button.n-button.n-button--primary-type.n-button--medium-type").click()

            # Read the response
            while True:
                chunk = driver.execute_script("""
if (window._message && window._message != window._last_message) {
    try {
        return window._message.substring(window._last_message.length);
    } finally {
        window._last_message = window._message;
    }
}
if (window._loadend) {
    return null;
}
return "";
""")
                if chunk:
                    # Yield the response chunk if it's not empty
                    yield chunk
                elif chunk != "":
                    # Break the loop if the response is empty but not null
                    break
                else:
                    # Sleep for 0.1 seconds before checking again
                    time.sleep(0.1)
