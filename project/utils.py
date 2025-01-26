import os
import json
from functools import wraps

from flask import Response, jsonify, request, stream_with_context
from openai import OpenAI
from .models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
)

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


def verify_api_key(f):
    """Decorator to verify API key in Authorization header"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        # Extract and verify API key
        provided_key = authorization[7:]  # Remove "Bearer " prefix
        if provided_key != os.getenv("API_KEY"):
            return jsonify({"error": "Forbidden: Invalid API key"}), 403

        return f(*args, **kwargs)

    return decorated_function


def create_streaming_response(request: ChatCompletionRequest) -> Response:
    """Create a streaming response for chat completions"""

    def generate():
        stream = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )

        for chunk in stream:
            try:
                yield f"data: {json.dumps(chunk.to_dict())}\n\n"
            except (ValueError, AttributeError) as e:
                # Skip malformed chunks rather than failing the entire stream
                continue

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


def create_standard_response(request: ChatCompletionRequest) -> Response:
    """Create a standard response from the OpenAI API response"""
    response = client.chat.completions.create(
        model=request.model,
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False,
    )
    if not hasattr(response, "choices") or not response.choices:
        raise ValueError("Invalid response format from API")

    return jsonify(
        ChatCompletionResponse(
            id=response.id,
            created=response.created,
            model=response.model,
            choices=[
                ChatCompletionResponseChoice(
                    index=choice.index,
                    message=ChatMessage(
                        role=choice.message.role, content=choice.message.content
                    ),
                    finish_reason=choice.finish_reason,
                    logprobs=getattr(choice, "logprobs", None),
                )
                for choice in response.choices
            ],
            usage=(
                {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
                if hasattr(response, "usage")
                else None
            ),
            system_fingerprint=getattr(response, "system_fingerprint", None),
        ).__dict__
    )
