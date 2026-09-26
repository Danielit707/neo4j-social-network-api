from fastapi import FastAPI
from neo4j.exceptions import Neo4jError
from app.database import check_connection, close_driver
from app.routes import analytics, auth, users, posts, visualization
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

app = FastAPI(title="Social Network API with Neo4j")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(visualization.router, prefix="/visual", tags=["Visualization"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "Welcome to the Social Network API!"}

@app.get("/health", tags=["Health"])
def health():
    try:
        check_connection()
    except Neo4jError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"status": "ok", "database": "ok"}

@app.on_event("shutdown")
def shutdown():
    close_driver()
