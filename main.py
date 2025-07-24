import sys
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) == 1:
        print("Error: expecting prompt")
        exit(1)
    else:
        prompt = sys.argv[1]
        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=prompt
        )
        print(response.text)
        tokprompt = response.usage_metadata.prompt_token_count
        tokresp = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {tokprompt}")
        print(f"Response tokens: {tokresp}")
        return 0

main()
