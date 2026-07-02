"""
TASK 1 : UNDERSTAND THE REQUEST-RESPONSE CYCLE

1. Journey of GET /api/courses/

Browser
   |
   | HTTP GET Request
   v
URL Router (urls.py)
   |
   | Matches URL pattern
   v
View (views.py)
   |
   | Executes business logic
   v
Model (models.py)
   |
   | Database Query
   v
Database
   |
   | Returns Data
   v
Model
   |
   v
View
   |
   | Creates HTTP Response
   v
Browser


2. Middleware

Middleware sits between the request and response process.

Request --> Middleware --> View --> Middleware --> Response

Example Built-in Middleware:

a) SecurityMiddleware
   - Adds security headers
   - Protects against common attacks
   - Helps enforce HTTPS

b) SessionMiddleware
   - Handles user sessions
   - Stores session data
   - Maintains login information


3. WSGI vs ASGI

WSGI (Web Server Gateway Interface)

- Synchronous
- Handles one request at a time per worker
- Traditional Django deployment
- Default interface used by Django

Examples:
- Gunicorn
- uWSGI

ASGI (Asynchronous Server Gateway Interface)

- Asynchronous
- Supports WebSockets
- Supports long-lived connections
- Suitable for real-time applications

Examples:
- Uvicorn
- Daphne

Django uses WSGI by default.

Switch to ASGI when:
- Chat applications
- Live notifications
- Real-time dashboards
- WebSocket communication


4. MVC to Django MVT Mapping

MVC Pattern

Model      -> Data Layer
View       -> User Interface
Controller -> Business Logic

Django MVT Pattern

Model      -> Model
View       -> Controller
Template   -> View

Mapping:

MVC Model      = Django Model
MVC View       = Django Template
MVC Controller = Django View

Explanation:

Model:
Stores and manages database data.

View:
Handles requests and business logic.

Template:
Displays data to the user.
""""""
PROJECT:
Entire Django website/application.

APP:
A reusable module inside a project.

Examples:
Project -> coursemanager
App -> courses

One project can contain multiple apps.
"""