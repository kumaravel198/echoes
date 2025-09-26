# gemini-test.py

from google import genai
import os  # Import the os module
import sys # Import sys for clean exit

# Check for the GEMINI_API_KEY environment variable
if not os.getenv("GEMINI_API_KEY"):
    print("Error: The GEMINI_API_KEY environment variable is not set.")
    print("To set it for the current terminal session, run this command (replace YOUR_API_KEY):")
    print("    export GEMINI_API_KEY=\"YOUR_API_KEY\"")
    print("\nTo set it permanently (for new terminal sessions), add the following line to your ~/.bashrc file and then run 'source ~/.bashrc':")
    # This prints the line the user should add to their .bashrc
    print("    echo 'export GEMINI_API_KEY=\"YOUR_API_KEY\"' >> ~/.bashrc")
    # Exit the script since the client won't be able to authenticate
    sys.exit(1)

# The client will automatically look for the GEMINI_API_KEY 
# environment variable, so you don't need to pass it explicitly.
client = genai.Client()

# This is now redundant since we check at the start, but kept for context:
# if not os.getenv("GEMINI_API_KEY"):
#     print("Error: GEMINI_API_KEY environment variable is not set.")
#     exit()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)