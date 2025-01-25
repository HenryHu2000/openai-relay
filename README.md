# OpenAI API Relay Server

A Flask-based proxy server that implements OpenAI's Chat Completion API specification, providing:
- API key authentication
- Streaming and standard response modes
- Structured request/response models
- Error handling and validation

## API Endpoint

`POST /v1/chat/completions`

### Request Headers
- `Authorization: Bearer {API_KEY}`
- `Content-Type: application/json`

### Request Body
```json
{
  "model": "deepseek-chat",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 100,
  "stream": false
}
```

### Example Request
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Setup

1. Create a `.env` file with your API key:
```bash
echo "API_KEY=your_api_key_here" > .env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:
```bash
FLASK_APP=project flask run --port=8000
```

The server will be available at `http://localhost:8000`

## Development

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

Run tests with:
```bash
pytest
