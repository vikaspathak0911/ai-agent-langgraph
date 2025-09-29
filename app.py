from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os

# This line adds the 'src' directory to Python's path.
# For Vercel, it's more reliable to move 'graph_enhanced.py' to the root directory
# and remove the sys.path modification. But let's try with this first.
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from graph_enhanced import agent, AgentState

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# === THIS IS THE NEW CODE I'VE ADDED ===
# A root endpoint to show a welcome message in the browser.
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "online", "message": "AI Agent API is running. Use the /chat endpoint to interact."})
# =======================================

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        user_input = data.get("user_input", "")
        if not user_input.strip():
            return jsonify({"error": "Empty message"}), 400

        state = AgentState(
            user_input=user_input,
            intent=None,
            tools_called=[],
            evidence=[],
            policy_decision=None,
            final_message=""
        )

        trace = agent.invoke(state)
        print(trace)

        if not isinstance(trace, dict):
            trace = dict(trace)

        final_message = trace.get("final_message", "")

        return jsonify({
            "final_message": final_message,
            "trace": trace,
            "status": "success"
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Something went wrong processing your request"
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "message": "Server is running"})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

