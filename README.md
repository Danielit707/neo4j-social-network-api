# Social Network API

A graph-based social network backend built with **FastAPI** and **Neo4j**. The
API supports user registration and authentication, social relationships,
interests, posts, comments, and interactive network visualization.

This project was developed at **Universidad del Norte** by:

- Daniel Cera
- Eliasib Pajaro
- Jesus Marquez
- Jesus Paternina

## Features

- Register users and authenticate with JWT bearer tokens.
- Store users, posts, comments, interests, and relationships as Neo4j graph
  entities.
- Create bidirectional friendships or one-way follows.
- Publish posts and comment on existing posts.
- Generate an interactive HTML visualization of a user's network up to two
  relationship levels deep.
- Explore the automatically generated OpenAPI documentation through FastAPI.

## Technology stack

- Python 3.8+
- FastAPI
- Uvicorn
- Neo4j
- PyJWT
- Passlib with bcrypt
- PyVis

## Prerequisites

- Python 3.8 or newer
- A running Neo4j instance (local or hosted)

## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/<your-username>/<your-repository>.git
   cd <your-repository>
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables. Create a `.env` file in the project
   root:

   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your-neo4j-password
   JWT_SECRET=replace-with-a-long-random-secret
   ```

   The application has local-development defaults for the Neo4j URI and user,
   but setting `NEO4J_PASSWORD` and `JWT_SECRET` explicitly is recommended.
   Do not commit `.env` or production secrets to the repository.

## Running the API

From the project root, start the development server:

```bash
uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>.

Interactive API documentation:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API overview

All protected endpoints require the token returned by `POST /auth/login`:

```text
Authorization: Bearer <access_token>
```

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| `GET` | `/` | Health/welcome response | No |
| `POST` | `/auth/register` | Register a user | No |
| `POST` | `/auth/login` | Obtain a JWT access token | No |
| `POST` | `/users/friend` | Create a friendship or follow relationship | Yes |
| `POST` | `/users/interest` | Add an interest to the current user | Yes |
| `POST` | `/posts/` | Create a post | Yes |
| `POST` | `/posts/comment` | Comment on a post | Yes |
| `GET` | `/visual/network/{email}` | Render a user's network graph | No |

Example registration request:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"ana\",\"email\":\"ana@example.com\",\"password\":\"change-me\"}"
```

## Project structure

```text
app/
├── main.py              # FastAPI application and route registration
├── config.py            # Environment-based configuration
├── database.py          # Neo4j driver and sessions
├── models/              # Graph operations
├── routes/              # API endpoints
├── schemas/             # Request/response schemas
└── utils/               # Authentication and graph helpers
```

## Authors

Daniel Cera, Eliasib Pajaro, Jesus Marquez, and Jesus Paternina  
Universidad del Norte

## License

No license has been specified yet. Add a license before distributing this
project for reuse.