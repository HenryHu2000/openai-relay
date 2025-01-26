from flask import jsonify, request
from .utils import verify_api_key, create_streaming_response, create_standard_response
from .models import ChatCompletionRequest


def init_routes(app):
    @app.route("/v1/chat/completions", methods=["POST"])
    @verify_api_key
    def create_chat_completion():
        """
        Handle chat completion requests with OpenAI API.

        Returns:
            Response: StreamingResponse for streaming requests
                      JSON response for standard requests
        """
        try:
            data = request.get_json()
            request_obj = ChatCompletionRequest(**data)

            if request_obj.stream:
                return create_streaming_response(request_obj)
            else:
                return create_standard_response(request_obj)

        except (ValueError, AttributeError) as e:
            return jsonify({"error": f"Invalid request format: {str(e)}"}), 400
        except ConnectionError as e:
            return jsonify({"error": "Service unavailable"}), 503
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
