from typing import List, Dict
from copy import deepcopy
import json

from smartgpt import gpt
from smartgpt import utils
from smartgpt.translator import Translator

class Reviewer:
    def __init__(self, model, translator: Translator):
        self.model = model
        self.translator = translator

    def review_plan_gen(self, messages: List[Dict]) -> Dict:
        review_prompt = """
Please review the prompt and your response, then answer the following questions in the provided format:
{
    "ambiguity_in_prompt": If there's no ambiguity in the prompt, write 'none'. If there is, please list the ambiguous elements.
    "not_self_contained_tasks": If there's a task description that isn't self-contained enough, please list it. If all are self-contained, write 'none'.
    "achieve_goal": Can the generated task lists meet the user's goal? true or false.
}
"""

        # Construct the messages for the review request
        messages = deepcopy(messages)
        messages.append({"role": "user", "content": review_prompt})

        # Send the review request to the LLM
        review_response = gpt.send_messages(messages, self.model)
        messages.append({"role": "assistant", "content": review_response})

        # write to files
        self._trace_llm_gen("plan", messages)
        return json.loads(review_response)

    def translate_to_instructions(self, task_info: Dict) -> str:
        instrs = self.translator.translate_to_instructions(task_info)
        return self.review_instructions_gen(instrs)

    def review_instructions_gen(self, instructions) -> str:
        review_prompt = ("Please scrutinize the instructions generated by Jarvis, ensuring they adhere to the following principles:\n"
                         "Each instruction's objective description should be sufficiently detailed and clear.\n"
                         "The args provided should offer comprehensive information, serving as self-contained input for each instruction execution.\n"
                         "Verify that Jarvis selects the appropriate instruction type to ensure the desired outcome can be achieved through execution.\n"
                         "The `jvm.get()` method must invariably be encapsulated within `jvm.eval()`. "
                         "This is crucial to assure correct evaluation within the 'content' field of the TextCompletion instruction.\n"
                         "The 'FetchWebContent' instruction cannot accept a local file path as a URL argument.\n"
                         "The 'RunPython' instruction should not contain jvm.eval().\n"
                         "\n"
                         "If all these stipulations are met, respond with 'Approved'. If not, please reproduce your response in YAML format:\n```yaml\n")

        messages = deepcopy(self.translator.messages)
        messages.append({"role": "user", "content": review_prompt})

        # Send the review request to the AI model
        review_response = gpt.send_messages(messages, self.model)
        messages.append({"role": "assistant", "content": review_response})

        # write to files
        self._trace_llm_gen(f"task_{self.translator.task_info['task_num']}", messages)

        if review_response.lower() == "approved":
            return instructions
        else:
            review_response = utils.strip_yaml(review_response)
            return review_response

    def _trace_llm_gen(self, step, messages):
        # Write to file in readable format (for human review)
        with open(f"review_{step}.txt", "w") as f:
            # Write the messages to the file in a readable format
            for message in messages:
                f.write(f"{message['role'].upper()}:\n")
                f.write(message['content'] + "\n\n")
