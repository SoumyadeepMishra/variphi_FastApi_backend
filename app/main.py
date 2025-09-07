from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.middleware.cors import add_cors_middleware
from app.routes import auth_route, user_route, post_route

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(post_route.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI MVC Template"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}





