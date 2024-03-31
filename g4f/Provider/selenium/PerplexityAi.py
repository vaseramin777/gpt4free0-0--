from __future__ import annotations  # Allows using class name in type hints

import time 

try:
    from selenium.webdriver.common.by import By  # Imports for Selenium WebDriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
except ImportError:
    pass

from ...typing import CreateResult, Messages  # Imports for custom types
from ..base_provider import AbstractProvider  # Imports for base class
from ..helper import format_prompt  # Imports for helper functions
from ...webdriver import WebDriver, WebDriverSession  # Imports for custom WebDriver classes

class PerplexityAi(AbstractProvider):
    url = "https://www.perplexity.ai"  # The URL of the Perplexity AI website
    working = True  # A flag indicating if the provider is working or not
    supports_gpt_35_turbo = True  # A flag indicating if the provider supports GPT-3.5-turbo model
    supports_stream = True  # A flag indicating if the provider supports streaming responses

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        timeout: int = 120,
        webdriver: WebDriver = None,
        virtual_display: bool = True,
        copilot: bool = False,
        **kwargs
    ) -> CreateResult:
        # The main function to create a completion using the Perplexity AI provider
        with WebDriverSession(webdriver, "", virtual_display=virtual_display, proxy=proxy) as driver:
            # Creates a WebDriver session and assigns it to the 'driver' variable
            prompt = format_prompt(messages)  # Formats the prompt using the helper function

            driver.get(f"{cls.url}/")  # Navigates the WebDriver to the Perplexity AI website
            wait = WebDriverWait(driver, timeout)  # Creates a WebDriverWait object for waiting for elements

            # Waits until the textarea for input is visible
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='Ask anything...']")))

            # Registers a WebSocket hook to capture messages
            script = """
            window._message = window._last_message = "";
            window._message_finished = false;
            const _socket_send = WebSocket.prototype.send;
            WebSocket.prototype.send = function(...args) {
                if (!window.socket_onmessage) {
                    window._socket_onmessage = this;
                    this.addEventListener("message", (event) => {
                        if (event.data.startsWith("42")) {
                            let data = JSON.parse(event.data.substring(2));
                            if (data[0] =="query_progress" || data[0] == "query_answered") {
                                let content = JSON.parse(data[1]["text"]);
                                if (data[1]["mode"] == "copilot") {
                                    content = content[content.length-1]["content"]["answer"];
                                    content = JSON.parse(content);
                                }
                                window._message = content["answer"];
                                if (!window._message_finished) {
                                    window._message_finished = data[0] == "query_answered";
                                }
                            }
                        }
                    });
                }
                return _socket_send.call(this, ...args);
            };
            """
            driver.execute_script(script)  # Executes the script to register the WebSocket hook

            if copilot:
                try:
                    # Checks for account
                    driver.find_element(By.CSS_SELECTOR, "img[alt='User avatar']")
                    # Enables copilot
                    driver.find_element(By.CSS_SELECTOR, "button[data-testid='copilot-toggle']").click()
                except:
                    raise RuntimeError("You need a account for copilot")

            # Submits the prompt
            driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Ask anything...']").send_keys(prompt)
            driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Ask anything...']").send_keys(Keys.ENTER)

            # Streams the response
            script = """
            if(window._message && window._message != window._last_message) {
                try {
                    return window._message.substring(window._last_message.length);
                } finally {
                    window._last_message = window._message;
                }
            } else if(window._message_finished) {
                return null;
            } else {
                return '';
            }
            """
            while True:
                chunk = driver.execute_script(script)
                if chunk:
                    # Yields the response chunk if it exists
                    yield chunk
                elif chunk != "":
                    # Breaks the loop if the response is empty
                    break
                else:
                    # Waits for a short period before checking again
                    time.sleep(0.1)
