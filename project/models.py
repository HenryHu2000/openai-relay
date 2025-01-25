from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class MessageContent:
    """Represents structured message content following OpenAI API"""
    type: str
    text: Optional[str] = None
    image_url: Optional[dict] = None
    function_call: Optional[dict] = None

@dataclass
class ChatMessage:
    """Represents a message in the chat conversation following OpenAI API"""
    role: str
    content: Union[str, List[Union[str, MessageContent]]]
    name: Optional[str] = None
    function_call: Optional[dict] = None

@dataclass
class ChatCompletionStreamOptions:
    """Options for streaming chat completions"""
    include_usage: Optional[bool] = False

@dataclass
class ChatCompletionRequest:
    """Request model matching OpenAI's API specification"""
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    stream_options: Optional[ChatCompletionStreamOptions] = None

@dataclass
class ChatCompletionResponseChoice:
    """Represents a single choice in the chat completion response"""
    index: int
    message: ChatMessage
    finish_reason: str
    logprobs: Optional[dict] = None

@dataclass
class ChatCompletionResponse:
    """Response model matching OpenAI's API specification"""
    id: str
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    object: str = "chat.completion"
    usage: Optional[dict] = None
    system_fingerprint: Optional[str] = None
