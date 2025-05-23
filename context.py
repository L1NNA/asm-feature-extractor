from dataclasses import dataclass
from transformers import AutoModelForCausalLM, AutoTokenizer

MODELS = {"codeqwen": "Qwen/Qwen2.5-Coder-0.5B-Instruct"}

BASE_PROMPT = """{instructions}

### Template ###
```json
{format}
```
"""


@dataclass
class Context:
    model: str  # Name of the model to use.
    prompt: str  # Directory containing the prompt and format to use

    def get_prompt(self, assembly: str):
        """
        Returns the prompt without the assembly code included
        """

        with open(
            f"prompts/{self.prompt}/instructions.txt", "r", encoding="utf-8"
        ) as instructions_file:
            instructions = instructions_file.read()

        with open(
            f"prompts/{self.prompt}/format.jsonc", "r", encoding="utf-8"
        ) as format_file:
            json_format = format_file.read()

        return [
            {
                "role": "system",
                "content": BASE_PROMPT.format(
                    instructions=instructions, format=json_format
                ),
            },
            {
                "role": "user",
                "content": f"```assembly\n{assembly}\n"
            }
        ]

    def get_model(self):
        """
        Return the model
        """

        return AutoModelForCausalLM.from_pretrained(
            MODELS[self.model],
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True,
        )

    def get_tokenizer(self):
        return AutoTokenizer.from_pretrained(MODELS[self.model], trust_remote_code=True)
