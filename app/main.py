from fastapi import FastAPI
from app.routes import auth, users, posts, visualization
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def root():
    return {"message": "Welcome to the Social Network API!"}
