import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class RefactorAgent:
    def __init__(self):
        # Setup google.generativeai with os.getenv("GEMINI_API_KEY")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")

    def refactor_code(self, code_content: str, language: str) -> str:
        # Prompt used: "You are a Senior Dev. Refactor this code to 'Diamond Standard': Strict Typing, JSDoc/Docstrings, Try/Catch blocks. Return ONLY the code."
        prompt = (
            f"You are a Senior Dev. Refactor this {language} code to 'Diamond Standard': "
            "Strict Typing, JSDoc/Docstrings, Try/Catch blocks. Return ONLY the code."
            f"\n\nCode:\n```{language}\n{code_content}\n```"
        )
        try:
            response = self.model.generate_content(prompt)
            content = response.text
            # Clean up markdown code blocks if present
            if content.startswith("```") and content.endswith("```"):
                lines = content.splitlines()
                # Remove first (```lang) and last (```) lines
                if len(lines) >= 2:
                    return "\n".join(lines[1:-1])
            return content
        except Exception as e:
            # Fallback or error logging
            print(f"Error refactoring code: {e}")
            return code_content
