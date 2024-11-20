import re
from flask import jsonify

def validate_email(email):
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def error_response(message, status_code):
    """Generate a standardized error response."""
    response = jsonify({"error": message})
    response.status_code = status_code
    return response

def success_response(message, data=None):
    """Generate a standardized success response."""
    response = {"message": message}
    if data:
        response["data"] = data
    return jsonify(response)

# Example usage of utility functions
if __name__ == "__main__":
    print(validate_email("test@example.com"))  # Should return True
    print(validate_email("invalid-email"))     # Should return False"# Helper functions" 
