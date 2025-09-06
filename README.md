# Notes API

A modern, secure note-taking API built with FastAPI and Firebase. This API provides full CRUD operations for notes with user authentication and authorization.

## Features

- **User Authentication** - Firebase ID Token based authentication
- **CRUD Operations** - Create, Read, Update, Delete notes
- **User Authorization** - Users can only access their own notes
- **Input Validation** - Pydantic models for data validation
- **Error Handling** - Standardized error responses with custom handlers
- **API Documentation** - Auto-generated Swagger UI
- **Health Check** - Monitoring endpoint (hidden from Swagger UI)
- **CORS Support** - Cross-origin resource sharing enabled
- **Clean Architecture** - Modular structure with core and modules
- **Logging System** - Configurable logging with different levels
- **Async Support** - All endpoints are asynchronous for better performance

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Firebase** - Authentication and Firestore database
- **Pydantic** - Data validation using Python type annotations
- **Python 3.13** - Programming language

## Project Structure

```
note-taking-backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Shared utilities and configurations
│   │   ├── __init__.py
│   │   ├── config.py           # Environment configuration
│   │   ├── firebase.py         # Firebase connection
│   │   ├── error_handling.py   # Custom exceptions and handlers
│   │   ├── response.py         # Response models
│   │   ├── logging.py          # Logging configuration
│   │   └── routes.py           # Route registration
│   └── modules/                # Business modules (Clean Architecture)
│       ├── auth/               # Authentication module
│       │   ├── __init__.py
│       │   ├── models.py       # Auth data models
│       │   ├── service.py      # Auth business logic
│       │   └── controller.py   # Auth API endpoints
│       └── notes/              # Notes module
│           ├── __init__.py
│           ├── models.py       # Note data models
│           ├── service.py      # Note business logic
│           └── controller.py   # Note API endpoints
├── .env                        # Environment variables
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── serviceAccountKey.json     # Firebase service account key
└── README.md                  # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd note-taking-backend
   ```

2. **Create virtual environment**

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   **Note:** If you get "python3: command not found" on macOS/Linux, try `python` instead of `python3`.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your Firebase configuration
   ```

5. **Configure Firebase**
   - Download your Firebase service account key (from Firebase Console -> Project Settings -> Service Accounts -> Generate new private key)
   - Place it in the project root as `serviceAccountKey.json`
   - Update `.env` file with your Firebase project details

6. **Run the application**

   **macOS/Linux:**
   ```bash
   uvicorn src.main:app --reload
   ```

   **Windows:**
   ```cmd
   uvicorn src.main:app --reload
   ```

   **Alternative (if uvicorn not found):**
   ```bash
   python -m uvicorn src.main:app --reload
   ```

7. **Access the API**
   - **Local Development:**
     - API: http://127.0.0.1:8000
     - Documentation: http://127.0.0.1:8000/docs
     - Health Check: http://127.0.0.1:8000/health
   - **Production (Live):**
     - API: https://note-taking-backend-04jp.onrender.com
     - Documentation: https://note-taking-backend-04jp.onrender.com/docs
     - Health Check: https://note-taking-backend-04jp.onrender.com/health

## API Documentation

### Base URL
- **Local Development:** `http://127.0.0.1:8000`
- **Production:** `https://note-taking-backend-04jp.onrender.com`

> **Note:** The root URL (`/`) only returns a welcome message. To access the interactive API documentation and testing interface, you must navigate to the `/docs` endpoint. This is the standard FastAPI behavior where Swagger UI is served at the `/docs` path.

### Authentication
All endpoints (except health check) require authentication using Firebase ID Token in the Authorization header:

```
Authorization: Bearer <your-firebase-id-token>
```

### Endpoints

#### Health Check
- **GET** `/health` - Check API health status (hidden from Swagger UI)

#### Authentication
- **GET** `/api/auth/me` - Get current user information
- **GET** `/api/auth/verify` - Verify authentication token

#### Notes
- **POST** `/api/Notes` - Create a new note
- **GET** `/api/Notes` - Get all user's notes
- **PUT** `/api/Notes/{note_id}` - Update a note
- **DELETE** `/api/Notes/{note_id}` - Delete a note

### Request/Response Format

#### Success Response Example
```json
{
  "success": true,
  "data": {
    "id": "note_id",
    "title": "Note Title",
    "content": "Note Content",
    "owner_uid": "user_id",
    "created_at": "2024-01-15T14:30:45Z",
    "updated_at": "2024-01-15T14:30:45Z"
  },
  "message": "Operation successful"
}
```

#### Error Response Example
```json
{
  "success": false,
  "statusCode": 404,
  "errorMessage": "Note not found",
  "details": null
}
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Firebase Configuration
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=./serviceAccountKey.json
FIREBASE_PROJECT_ID=your-project-id

# App Settings
APP_NAME=Notes API
DEBUG=True
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///./notes.db
```

## Architecture

This project follows **Clean Architecture** principles with a modular structure:

- **Core Module** - Shared utilities, configurations, and common functionality
- **Modules** - Business logic organized by domain (auth, notes)
- **Controller Layer** - Handles HTTP requests and responses
- **Service Layer** - Contains business logic and data operations
- **Model Layer** - Data validation and serialization with Pydantic

## Security Features

- **Secure Authentication** - Firebase ID token based authentication
- **Data Protection** - Users can only access their own data
- **Input Sanitization** - All inputs are validated and sanitized
- **Error Security** - No sensitive information leaked in error responses

## Flutter Integration

### Base URL Configuration
```dart
// In your Flutter app
const String baseUrl = 'https://note-taking-backend-04jp.onrender.com';
```

### HTTP Headers
```dart
final headers = {
  'Authorization': 'Bearer $firebaseToken',
  'Content-Type': 'application/json',
};
```

### Example API Call
```dart
// Get user's notes
final response = await http.get(
  Uri.parse('$baseUrl/api/Notes'),
  headers: headers,
);
```

## Testing

### Using Swagger UI
1. **Local Development:** Go to http://127.0.0.1:8000/docs
2. **Production:** Go to https://note-taking-backend-04jp.onrender.com/docs
3. Click "Authorize" button
4. Enter your Firebase ID token
5. Test the endpoints

## Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request - Validation Error |
| 401  | Unauthorized - Invalid/Expired Token |
| 403  | Forbidden - Access Denied |
| 404  | Not Found - Resource Not Found |
| 422  | Validation Error - Invalid Input |
| 500  | Internal Server Error |

## Author

**Osmangazi YILDIZ**
- GitHub: [@osmangaziyildiz](https://github.com/osmangaziyildiz)

---

**Note**: This API is designed for case study purposes with FastAPI and Firebase.