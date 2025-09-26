# gemini-test.py

from google import genai
import os  # Import the os module

# The client will automatically look for the GEMINI_API_KEY 
# environment variable, so you don't need to pass it explicitly.
client = genai.Client()

# Optional: Verify the key is loaded (for debugging)
if not os.getenv("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable is not set.")
    exit()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)