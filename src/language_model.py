from llama_cpp import Llama




class LanguageModel:
    def __init__(self, prompt=None):
        self.llm = Llama.from_pretrained(
            repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
            filename="*q8_0.gguf",
            verbose=False
        )
        if prompt is not None:
            self.prompt = prompt
        else:
            self.prompt = ("You are Jarvis, a highly intelligent and efficient AI assistant, designed to help users with"
                           " tasks, answer questions, and provide accurate information in a polite and professional "
                           "manner. Your goal is to be as helpful as possible. "
                           "You speak only in English."
                           " Provide brief and relevant answers, avoiding unnecessary details."
                           " Stick to the main point and keep responses very short.")

    def make_question(self, text):
        llm_prompt = self.prompt + "\nQ: {} \nA: ".format(text)
        output = self.llm(
            llm_prompt,  # Prompt
            max_tokens=64,  # Generate up to 32 tokens, set to None to generate up to the end of the context window
            stop=["Q:"],  # Stop generating just before the model would generate a new question
            echo=True  # Echo the prompt back in the output
        )  # Generate a completion, can also call create_completion
        return output['choices'][0]['text'][len(llm_prompt):]
