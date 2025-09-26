# gemini-test.py

from google import genai
import os
import sys
import time

# Define the default model
DEFAULT_MODEL = "gemini-2.5-flash"
MODEL_ARG_FLAG = "--model" # Flag to look for the model name

# --- 1. API Key Check (Unchanged) ---
if not os.getenv("GEMINI_API_KEY"):
    print("Error: The GEMINI_API_KEY environment variable is not set.")
    print("To set it for the current terminal session, run this command (replace YOUR_API_KEY):")
    print("    export GEMINI_API_KEY=\"YOUR_API_KEY\"")
    print("\nTo set it permanently (for new terminal sessions), add the following line to your ~/.bashrc file and then run 'source ~/.bashrc':")
    print("    echo 'export GEMINI_API_KEY=\"YOUR_API_KEY\"' >> ~/.bashrc")
    sys.exit(1)

# --- 2. Get Model and Contents from Command Line ---

# Initialize variables
model_name = DEFAULT_MODEL
prompt_content_parts = []
i = 1

# Check for the optional model argument
if len(sys.argv) > 1 and sys.argv[1] == MODEL_ARG_FLAG:
    if len(sys.argv) < 3:
        print(f"Error: No model name provided after '{MODEL_ARG_FLAG}'.")
        print(f"Usage: python gemini-test.py {MODEL_ARG_FLAG} <MODEL_NAME> \"<YOUR_PROMPT_HERE>\"")
        sys.exit(1)
    
    # Set the model name from the argument
    model_name = sys.argv[2]
    print(f"Using specified model: {model_name}")
    i = 3 # Start reading prompt content from the 3rd index onwards

# If the flag wasn't present, the model remains the default, and we start reading prompt from index 1.
elif len(sys.argv) == 1:
    print("Error: No prompt provided.")
    print(f"Usage: python gemini-test.py \"<YOUR_PROMPT_HERE>\"")
    print(f"Optional: python gemini-test.py {MODEL_ARG_FLAG} <MODEL_NAME> \"<YOUR_PROMPT_HERE>\"")
    sys.exit(1)

# Collect all remaining arguments as the prompt content
prompt_content = " ".join(sys.argv[i:])

if not prompt_content:
    print("Error: No prompt provided after model argument.")
    print(f"Usage: python gemini-test.py {MODEL_ARG_FLAG} <MODEL_NAME> \"<YOUR_PROMPT_HERE>\"")
    sys.exit(1)

# --- 3. Run Gemini Client with Timer ---
client = genai.Client()

print(f"Sending request to '{model_name}' for: '{prompt_content[:50]}...'")
print("-" * 20)

# Start the timer
start_time = time.time()

# Make the API call
response = client.models.generate_content(
    model=model_name, # Use the dynamic model_name
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

# Examples
# python gemini-test.py "How much caffeine is in a McDonalds medium black coffee"
# python gemini-test.py --model gemini-2.5-pro "What is the difference between a diode and a transistor?"
# python gemini-test.py --model gemini-2.5-flash "What is the difference between a diode and a transistor?"
# python gemini-test.py --model gemini-2.5-flash-lite "What is the difference between a diode and a transistor?"