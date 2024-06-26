from __future__ import annotations  # Allows forward references in type hints

import time  # Import time module for sleeping
import os  # Import os module for environment variable access

# Import necessary Selenium modules
try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
except ImportError:
    pass

# Import custom types, base_provider, and helper modules
from ...typing import CreateResult, Messages
from ..base_provider import AbstractProvider
from ..helper import format_prompt
from ...webdriver import WebDriver, WebDriverSession

class Bard(AbstractProvider):
    # Class variables
    url = "https://bard.google.com"
    working = True
    needs_auth = True

    @classmethod
    def create_completion(
            cls,
            model: str,
            messages: Messages,
            stream: bool,
            proxy: str = None,
            webdriver: WebDriver = None,
            user_data_dir: str = None,
            headless: bool = True,
            **kwargs
    ) -> CreateResult:
        # Format the prompt using the helper function
        prompt = format_prompt(messages)

        # Create a WebDriverSession object
        session = WebDriverSession(webdriver, user_data_dir, headless, proxy=proxy)

        # Context manager to handle WebDriver session
        with session as driver:
            try:
                # Navigate to the Bard chat URL
                driver.get(f"{cls.url}/chat")

                # Wait for the textarea to be visible
                wait = WebDriverWait(driver, 10 if headless else 240)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ql-editor.textarea")))
            except:
                # If the textarea is not found, reopen the browser for login
                if not webdriver:
                    driver = session.reopen()
                    driver.get(f"{cls.url}/chat")
                    login_url = os.environ.get("G4F_LOGIN_URL")
                    if login_url:
                        yield f"Please login: [Google Bard]({login_url})\n\n"
                    wait = WebDriverWait(driver, 240)
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ql-editor.textarea")))
                else:
                    raise RuntimeError("Prompt textarea not found. You may not be logged in.")

            # Add a hook in XMLHttpRequest
            script = """
            const _http_request_open = XMLHttpRequest.prototype.open;
            window._message = "";
            XMLHttpRequest.prototype.open = function(method, url) {
                if (url.includes("/assistant.lamda.BardFrontendService/StreamGenerate")) {
                    this.addEventListener("load", (event) => {
                        window._message = JSON.parse(JSON.parse(this.responseText.split("\\n")[3])[0][2])[4][0][1][0];
                    });
                }
                return _http_request_open.call(this, method, url);
            }
            """
            driver.execute_script(script)

            # Find the textarea and send the prompt lines
            textarea = driver.find_element(By.CSS_SELECTOR, "div.ql-editor.textarea")
            lines = prompt.splitlines()
            for idx, line in enumerate(lines):
                textarea.send_keys(line)
                if (len(lines) - 1 != idx):
                    textarea.send_keys(Keys.SHIFT + "\n")
            textarea.send_keys(Keys.ENTER)

            # Continuously yield chunks of the response
            while True:
                chunk = driver.execute_script("return window._message;")
                if chunk:
                    yield chunk
                    return
                else:
                    time.sleep(0.1)
