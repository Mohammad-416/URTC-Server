from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import string
import time
from typing import Optional
from login import login


app = FastAPI(title="URTC Dummy Server", version="1.0.0")

# Enable CORS for Unity communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and Response models
class StartCollaborationRequest(BaseModel):
    project_name: str
    user_email: str

class StartCollaborationResponse(BaseModel):
    success: bool
    message: str
    project_id: Optional[str] = None
    repo_url: Optional[str] = None

# Helper functions
def generate_project_id() -> str:
    """Generate a random project ID"""
    timestamp = str(int(time.time()))
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"proj_{timestamp}_{random_part}"

def generate_repo_url(project_name: str, user_email: str) -> str:
    """Generate a dummy GitHub repo URL"""
    # Extract username from email (before @)
    username = user_email.split('@')[0].lower()
    # Clean project name for URL
    clean_project_name = project_name.replace(' ', '-').lower()
    return f"https://github.com/{username}/{clean_project_name}"

def simulate_processing_delay():
    """Simulate server processing time"""
    time.sleep(random.uniform(1, 3))  # Random delay between 1-3 seconds



# API Endpoints
@app.get("/")
async def root():
    return {"message": "URTC Dummy Server is running!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# @app.get("/api/authorize")
# async def authorize(email: str):
#     if email is None or "@" not in email:
#         response = False
#         message = "Email is required and must be valid"
#         raise HTTPException(
#             status_code=400, 
#             detail="Email is required and must be valid"
#         )
#     else:
#         response = login(email)
#         if not response:
#             message = "Authorization failed. No Unity account found with this email."
#             raise HTTPException(
#                 status_code=401, 
#                 detail=message
#             )
#         message = "Authorization successful. You can now start collaboration."
#     return {"success": response, "message": message}

@app.post("/api/start-collaboration", response_model=StartCollaborationResponse)
async def start_collaboration(request: StartCollaborationRequest):
    """
    Dummy endpoint that simulates the collaboration start process
    """
    
    # Validate input
    if not request.project_name or not request.user_email:
        raise HTTPException(
            status_code=400, 
            detail="Project name and user email are required"
        )
    
    if "@" not in request.user_email:
        raise HTTPException(
            status_code=400, 
            detail="Invalid email format"
        )
    
    # Simulate processing time
    simulate_processing_delay()
    
    # Simulate random failures (10% chance)
    if random.random() < 0.1:
        error_messages = [
            "GitHub authentication failed",
            "Repository creation failed",
            "Database connection error",
            "User not found on GitHub"
        ]
        raise HTTPException(
            status_code=500, 
            detail=random.choice(error_messages)
        )
    
    # Generate dummy response data
    project_id = generate_project_id()
    repo_url = generate_repo_url(request.project_name, request.user_email)
    
    # Success response
    return StartCollaborationResponse(
        success=True,
        message=f"Collaboration started successfully for project '{request.project_name}'",
        project_id=project_id,
        repo_url=repo_url
    )

@app.post("/api/add-collaborator")
async def add_collaborator(collaborator_email: str, project_id: str):
    """
    Dummy endpoint for adding collaborators (for future use)
    """
    simulate_processing_delay()
    
    if random.random() < 0.2:  # 20% failure rate
        raise HTTPException(
            status_code=404, 
            detail="User not found or already a collaborator"
        )
    
    return {
        "success": True,
        "message": f"Collaborator {collaborator_email} added to project {project_id}"
    }

@app.get("/api/projects/{project_id}")
async def get_project_info(project_id: str):
    """
    Dummy endpoint to get project information
    """
    return {
        "project_id": project_id,
        "project_name": f"Unity Project {project_id[-6:]}",
        "status": "active",
        "collaborators": random.randint(1, 5),
        "created_at": time.time() - random.randint(3600, 86400)  # Random time in last day
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=10000,
        reload=True,
        log_level="info"
    )

# Additional dummy data for testing
SAMPLE_USERS = [
    "john.doe@example.com",
    "jane.smith@github.com",
    "developer@unity.com",
    "coder@test.org"
]

SAMPLE_PROJECTS = [
    "AwesomeGame",
    "Unity3D-Project",
    "MyFirstGame",
    "CollaborationTest",
    "GameDev2024"
]