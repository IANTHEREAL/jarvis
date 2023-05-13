
from dataclasses import dataclass
import io
import subprocess
import inspect
import json
import gpt
from spinner import Spinner
from typing import Union
from abc import ABC
from abc import ABC
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


@dataclass(frozen=True)
class Action(ABC):
    @classmethod
    def from_dict(cls, data: Union[str, dict]):
        if isinstance(data, str):
            data = json.loads(data)  # Parse the input string into a dictionary

        action_type = data.get("type")

        if action_type is None or action_type not in ACTION_CLASSES:
            return None

        action_class = ACTION_CLASSES[action_type]

        # Get the constructor parameters for the action class
        constructor_params = inspect.signature(action_class).parameters

        # Create a dictionary of constructor arguments from the JSON data
        constructor_args = {}
        for param_name, _ in constructor_params.items():
            if param_name != "self" and param_name in data:
                constructor_args[param_name] = data[param_name]

        return action_class(**constructor_args)



    def key(self) -> str:
        raise NotImplementedError

    def short_string(self) -> str:
        raise NotImplementedError

    def run(self) -> str:
        """Returns what jarvis should learn from running the action."""
        raise NotImplementedError



@dataclass(frozen=True)
class SearchOnlineAction(Action):
    query: str

    def key(self) -> str:
        return "SEARCH_ONLINE"

    def short_string(self) -> str:
        return f"Search online for `{self.query}`."

    def run(self) -> str:
        response = search(self.query, num=10)
        if response is None:
            return f"SearchOnlineAction RESULT: The online search for `{self.query}` appears to have failed."
        result = "\n".join([str(url) for url in response])
        print(f"SearchOnlineAction RESULT: The online search for `{self.query}` returned the following URLs:\n{result}")
        return result


@dataclass(frozen=True)
class ExtractInfoAction(Action):
    url: str
    instructions: str

    def key(self) -> str:
        return "EXTRACT_INFO"

    def short_string(self) -> str:
        return f"Extract info from `{self.url}`: {self.instructions}."

    def run(self) -> str:
        with Spinner("Reading website..."):
            html = self.get_html(self.url)
        text = self.extract_text(html)
        print(f"RESULT: The webpage at `{self.url}` was read successfully.")
        user_message_content = f"{self.instructions}\n\n```\n{text[:10000]}\n```"
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You will be given instructions to extract some information from the contents of a website. Do your best to follow the instructions and extract the info.",
            },
            {"role": "user", "content": user_message_content},
        ]
        request_token_count = gpt.count_tokens(messages)
        max_response_token_count = gpt.COMBINED_TOKEN_LIMIT - request_token_count
        with Spinner("Extracting info..."):
            extracted_info = gpt.send_message(messages, max_response_token_count, model=gpt.GPT_3_5_TURBO)
        print("ExtractInfoAction RESULT: The info was extracted successfully.")
        return extracted_info

    def get_html(self, url: str) -> str:
        options = ChromeOptions()
        options.headless = True
        browser = ChromeWebDriver(executable_path=ChromeDriverManager().install(), options=options)
        browser.get(url)
        html = browser.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        browser.quit()
        return html

    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        return text


@dataclass(frozen=True)
class RunPythonAction(Action):
    path: str
    timeout: int  # in seconds
    cmd_args: str
    code:str

    def key(self) -> str:
        return "RUN_PYTHON"

    def short_string(self) -> str:
        return f"Run Python file `{self.path} {self.cmd_args}`."

    def run(self) -> str:
        # write code to path and run
        with io.open(self.path, mode="w", encoding="utf-8") as file:
            file.write(self.code)
        with subprocess.Popen(
             f"python {self.path} {self.cmd_args}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ) as process:
            try:
                exit_code = process.wait(timeout=self.timeout)  # Add the timeout argument
                output = process.stdout.read() if process.stdout else ""
                output = f"\nPython script `python {self.path} {self.cmd_args}` returned exit code {exit_code}, stdout of process:\n{output}"
                if exit_code != 0:
                    output += f"\n\nPython script code:\n{self.code}"
                print(f"python {self.path} {self.cmd_args}` returned exit code {exit_code}, stdout of process:\n{output}")
                return output
            except subprocess.TimeoutExpired:
                process.kill()
                return f"RunPythonAction failed: The Python script at `{self.path} {self.cmd_args}` timed out after {self.timeout} seconds."


@dataclass(frozen=True)
class ShutdownAction(Action):
    message: str

    def key(self):
        return "SHUTDOWN"

    def short_string(self) -> str:
        return f"Shutdown:{self.message}"

    def run(self) -> str:
        # This action is treated specially, so this can remain unimplemented.
        raise NotImplementedError
    
        
# Helper function to populate the ACTION_CLASSES dictionary
def _populate_action_classes(action_classes):
    result = {}
    for action_class in action_classes:
        # Get the parameters of the __init__() method for this action class
        init_params = inspect.signature(action_class.__init__).parameters

        # Construct a dictionary of default argument values for the __init__() method
        default_args = {}
        for param in init_params.values():
            if param.name != "self":
                default_args[param.name] = param.default

        # Create an instance of the action class with the default arguments
        action_instance = action_class(**default_args)

        # Add the action class to the result dictionary, using the key returned by the key() method
        result[action_instance.key()] = action_class

    return result       

ACTION_CLASSES = _populate_action_classes([
    RunPythonAction,
    ShutdownAction,
    ExtractInfoAction,
    SearchOnlineAction,
])
