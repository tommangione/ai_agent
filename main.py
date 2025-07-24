import sys
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
client = genai.Client(api_key=api_key)
from google.genai import types

if len(sys.argv) == 1:
    print("Error: expecting prompt")
    exit(1)

if len(sys.argv) > 2 and sys.argv[2] != "--verbose":
    print("Error: too many arguments.")
    exit(1)

if len(sys.argv) > 3:
    print("Error: too many arguments. Please enclose one prompt at a time in quotation marks. You may use optional argument --verbose after prompt for token data.")
    exit(1)

messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

def main():
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages
    )
    print(response.text)
    tokprompt = response.usage_metadata.prompt_token_count
    tokresp = response.usage_metadata.candidates_token_count
    for arg in sys.argv:
        if arg == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {tokprompt}")
            print(f"Response tokens: {tokresp}")

main()
