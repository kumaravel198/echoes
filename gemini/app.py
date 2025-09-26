# app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import time
from google import genai
from google.genai.errors import APIError 


# --- Flask Application Setup ---

# The application loads the client from the environment variable GEMINI_API_KEY.
app = Flask(__name__, static_folder='static_html') 
CORS(app) 

# --- Gemini API Client Initialization ---
# Initialize GEMINI_CLIENT to None.
GEMINI_CLIENT = None 
try:
    # The client automatically uses the GEMINI_API_KEY environment variable.
    GEMINI_CLIENT = genai.Client()
    print("Gemini client initialized successfully.")
except Exception as e:
    # Print error but allow the application to start.
    print(f"Error initializing Gemini client: {e}", file=sys.stderr)


@app.route('/', defaults={'path': ''})
def serve_static(path):
    """Serves the HTML frontend."""
    # This serves the frontend file 'gemini_frontend.html'
    return send_from_directory(app.static_folder, 'gemini_frontend.html')

                                                                                                                                                                            
@app.route('/gemini_call', methods=['POST'])
def gemini_call():
    """API endpoint to handle Gemini API calls."""
    data = request.get_json()
    prompt = data.get('prompt', '')
    model_name = data.get('model', 'gemini-2.5-flash')
    
    if not prompt:
        return jsonify({"error": "Prompt cannot be empty."}), 400

    # IMPROVEMENT: Check if the client failed to initialize at startup
    if GEMINI_CLIENT is None:
        # Returns a 500 status if the client object itself is missing.
        return jsonify({
            "error": "Internal Server Error: Gemini client failed to initialize at startup."
        }), 500
    
    if not os.getenv("GEMINI_API_KEY"):
        # Returns a 500 status if the API key is missing (even if the client initialized).
        return jsonify({
            "error": "GEMINI_API_KEY environment variable is not set on the server."
        }), 500

    try:
        start_time = time.time()
        
        # Use the initialized client
        response = GEMINI_CLIENT.models.generate_content(
            model=model_name,
            contents=prompt
        )

        end_time = time.time()
        duration = end_time - start_time
        
        response_text = f"{response.text}\n\n"
        response_text += "=" * 30 + "\n"
        response_text += f"Response received in: {duration:.2f} seconds.\n"
        response_text += "=" * 30
        
        return jsonify({"result": response_text})

    except APIError as e:
        print(f"Gemini API Error: {e}", file=sys.stderr)
        return jsonify({"error": f"Gemini API Error: {e}"}), 502
    except Exception as e:
        print(f"Internal server error: {e}", file=sys.stderr)
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == '__main__':
    # Binds to 0.0.0.0 so it's accessible outside the container
    app.run(debug=True, host='0.0.0.0', port=5000)