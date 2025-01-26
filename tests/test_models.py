import pytest
from project.models import (
    MessageContent,
    ChatMessage,
    ChatCompletionStreamOptions,
    ChatCompletionRequest,
    ChatCompletionResponseChoice,
    ChatCompletionResponse,
)


def test_message_content_creation():
    # Test basic text content
    text_content = MessageContent(type="text", text="Hello")
    assert text_content.type == "text"
    assert text_content.text == "Hello"
    assert text_content.image_url is None
    assert text_content.function_call is None

    # Test image content
    image_content = MessageContent(
        type="image_url", image_url={"url": "https://example.com/image.png"}
    )
    assert image_content.type == "image_url"
    assert image_content.image_url["url"] == "https://example.com/image.png"


def test_chat_message_creation():
    # Test simple text message
    text_message = ChatMessage(role="user", content="Hello")
    assert text_message.role == "user"
    assert text_message.content == "Hello"
    assert text_message.name is None
    assert text_message.function_call is None

    # Test complex content with MessageContent
    complex_content = [
        MessageContent(type="text", text="Hello"),
        MessageContent(
            type="image_url", image_url={"url": "https://example.com/image.png"}
        ),
    ]
    complex_message = ChatMessage(role="assistant", content=complex_content)
    assert len(complex_message.content) == 2
    assert isinstance(complex_message.content[0], MessageContent)
    assert complex_message.content[1].type == "image_url"


def test_chat_completion_request():
    messages = [ChatMessage(role="user", content="Hello")]
    request = ChatCompletionRequest(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=100,
        stream=True,
        stream_options=ChatCompletionStreamOptions(include_usage=True),
    )

    assert request.model == "gpt-4"
    assert len(request.messages) == 1
    assert request.temperature == 0.7
    assert request.max_tokens == 100
    assert request.stream is True
    assert request.stream_options.include_usage is True


def test_chat_completion_response():
    message = ChatMessage(role="assistant", content="Hello there")
    choice = ChatCompletionResponseChoice(
        index=0, message=message, finish_reason="stop"
    )
    response = ChatCompletionResponse(
        id="chatcmpl-123",
        created=1677652288,
        model="gpt-4",
        choices=[choice],
        usage={"prompt_tokens": 10, "completion_tokens": 20},
    )

    assert response.id == "chatcmpl-123"
    assert response.model == "gpt-4"
    assert len(response.choices) == 1
    assert response.choices[0].message.content == "Hello there"
    assert response.usage["prompt_tokens"] == 10


def test_required_fields():
    # Test that required fields raise TypeError if missing
    with pytest.raises(TypeError):
        MessageContent()  # Missing type

    with pytest.raises(TypeError):
        ChatMessage()  # Missing role and content

    with pytest.raises(TypeError):
        ChatCompletionRequest()  # Missing model and messages

    with pytest.raises(TypeError):
        ChatCompletionResponse()  # Missing id, created, model, and choices


def test_optional_fields():
    # Test that optional fields can be omitted
    message = ChatMessage(role="user", content="Hi")
    assert message.name is None
    assert message.function_call is None

    request = ChatCompletionRequest(model="gpt-4", messages=[message])
    assert request.temperature == 1.0  # Default value
    assert request.max_tokens is None
    assert request.stream is False
    assert request.stream_options is None
