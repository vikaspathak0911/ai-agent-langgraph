from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from graph_enhanced import agent, AgentState

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_input = data.get("user_input", "")
        
        if not user_input.strip():
            return jsonify({"error": "Empty message"}), 400

        # Create agent state
        state = AgentState(
            user_input=user_input,
            intent=None,
            tools_called=[],
            evidence=[],
            policy_decision=None,
            final_message=""
        )

        trace = agent.invoke(state)

        # Ensure trace is a plain dict
        if not isinstance(trace, dict):
            trace = dict(trace)

        # Extract final_message
        final_message = trace.get("final_message", "")

        # Return structured response
        return jsonify({
            "final_message": final_message,
            "trace": trace,  # keep full trace for debugging
            "status": "success"
        })

        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error in chat endpoint: {str(e)}")
        
        # Return error response
        return jsonify({
            "error": "Internal server error",
            "message": "Something went wrong processing your request"
        }), 500

# Add a health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "message": "Server is running"})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)