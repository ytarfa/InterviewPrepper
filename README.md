# Interview Practice Assistant API

A backend service built with FastAPI and LangChain.

The Interview Practice Assistant API aims to help users strengthen their interview skills by:
- Generating tailored interview questions that align with the user’s resume and target job description
- Offering constructive, actionable feedback on responses, allowing users to learn and refine their answers in real time


## Running the Application

### Prerequisites
- Python 3.9 or higher
- pip

### Installation Steps

1. Clone the repository
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment (recommended)

```
# Windows
python -m venv venv
venv\Scripts\activate
```

```
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Create a .env file in the project root and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

4. Install dependencies

```pip install -r requirements.txt```

### Running the Application

5. Start the FastAPI server

```
uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000

### API Documentation

FastAPI automatically generates interactive API documentation:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

## Features Status

### Core Functionality
- [x] Resume Analysis
  - [x] Extract information from resume
  - [ ] Allow users to edit extracted resume information
  - [ ] Support resume-only interview preparation

- [x] Job Description Analysis
  - [x] Extract information from job description
  - [ ] Allow users to edit extracted job description
  - [ ] Support job description-only interview preparation

### Interview Process
- [x] Question Generation & Evaluation
  - [x] Generate relevant interview questions
  - [x] Evaluate user responses
  - [ ] Support answer retry after feedback
  - [ ] Enable follow-up questions to previous responses

### Customization Options
- [ ] Question Types
  - [ ] Separate behavioral and technical questions
  - [ ] Let users choose question type
  - [ ] Track skills/experiences covered in questions

- [ ] Interview Flow Control
  - [ ] Allow users to select topics for upcoming questions
  - [ ] Provide progress tracking for covered skills

### Skill Research Integration
- [ ] Leverage LangChain tools to research user skills
  - [ ] Automatically retrieve information about user's skills
  - [ ] Identify common interview questions for each skill
  - [ ] Incorporate research results into question generation

## API Endpoints

### Get All Sessions
```http
GET /api/sessions/
```
Retrieves all interview preparation sessions.

**Response**: List of sessions (200 OK)

### Create New Session
```http
POST /api/sessions/
```
Creates a new interview preparation session.

**Response**: Session details (200 OK)

### Delete All Sessions
```http
DELETE /api/sessions/
```
Removes all interview preparation sessions from the system.

**Response**: Confirmation of deletion (200 OK)

### Get Specific Session
```http
GET /api/sessions/{session_id}
```
Retrieves details for a specific interview session.

**Parameters**:
- `session_id` (path parameter, required): Unique identifier for the session

**Response**: Session details (200 OK)

### Delete Specific Session
```http
DELETE /api/sessions/{session_id}
```
Removes a specific interview session.

**Parameters**:
- `session_id` (path parameter, required): Unique identifier for the session

**Response**: Confirmation of deletion (200 OK)

### Handle Message
```http
POST /api/sessions/message
```
Processes messages within an interview session. Handling the interview Q&A interaction.

**Request Body**:
```json
{
  "session_id": "string",
  "message": "string"
}
```

**Response**: Array of messages
```json
[
  {
    "content": "string",
    "type": "user" | "system"
  }
]
```


