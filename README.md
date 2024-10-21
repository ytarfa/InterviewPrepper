# Interview Practice Assistant API (v0.1.0)

A FastAPI-based backend service that uses LangChain and Claude to create an interactive interview practice experience. This initial version provides basic functionality for conducting mock interviews with AI-generated questions and feedback.

## Overview

The Interview Practice Assistant helps users prepare for job interviews by:

- Generating relevant technical and behavioral questions based on the user's resume and target job description
- Providing constructive feedback on answers
- Offering follow-up questions to dive deeper into topics
- Maintaining context throughout the interview session

## API Endpoints

### Start Interview

```http
POST /api/interview/start
```

Initiates a new interview session with the provided resume and job description.

### Submit Answer

```http
POST /api/interview/answer
```

Submits an answer for evaluation and optionally requests a follow-up question.

## Feature Checklist

Features:

- [x] Question generation based on resume and job description
- [x] Answer evaluation with constructive feedback
- [x] Follow-up question generation
- [ ] Extract skills from job description and YoE from job description and resume
- [ ] Interview history tracking
- [ ] Progress tracking and analytics
- [ ] Custom prompt templates
- [ ] Question banks
- [ ] Multiple interview formats (behavioral, technical, etc.)
