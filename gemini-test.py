# gemini-test.py

from google import genai
import os
import sys
import time  # Import the time module for timing

# --- 1. API Key Check (Unchanged) ---
if not os.getenv("GEMINI_API_KEY"):
    print("Error: The GEMINI_API_KEY environment variable is not set.")
    print("To set it for the current terminal session, run this command (replace YOUR_API_KEY):")
    print("    export GEMINI_API_KEY=\"YOUR_API_KEY\"")
    print("\nTo set it permanently (for new terminal sessions), add the following line to your ~/.bashrc file and then run 'source ~/.bashrc':")
    print("    echo 'export GEMINI_API_KEY=\"YOUR_API_KEY\"' >> ~/.bashrc")
    sys.exit(1)

# --- 2. Get Contents from Command Line (Unchanged) ---
if len(sys.argv) < 2:
    print("Error: No prompt provided.")
    print("Usage: python gemini-test.py \"<YOUR_PROMPT_HERE>\"")
    sys.exit(1)

prompt_content = " ".join(sys.argv[1:])

# --- 3. Run Gemini Client with Timer ---
client = genai.Client()

print(f"Sending request for: '{prompt_content[:50]}...'")
print("-" * 20)

# Start the timer
start_time = time.time()

# Make the API call
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt_content
)

# Stop the timer
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

# Print the response text first
print(response.text)

# Print the timing information
print("\n" + "=" * 30)
print(f"Response received in: {duration:.2f} seconds.")
print("=" * 30)