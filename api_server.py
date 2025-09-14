












import os
import json
import asyncio
import hashlib
import secrets
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from role_coordinator import RoleCoordinator
from roles import ProductManager, Architect, Engineer, QaEngineer
from roles.unified_roles import AnalystArchitect, DeveloperEngineer, TesterQa
from roles.task_decomposer import TaskDecomposer
from roles.reviewer import Reviewer
from roles.documentation_specialist import DocumentationSpecialist
from roles.project_manager import ProjectManager
from roles.git_integrator import GitIntegrator
from roles.test_runner import TestRunner
from roles.agent_monitor import AgentMonitor

# Initialize FastAPI app
app = FastAPI()

# Database setup (SQLite)
import sqlite3

DATABASE_URL = "multi_agent_coder.db"
SECRET_KEY = "your-secret-key-here"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            owner_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users (id)
        )
    ''')

    # Create agents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')

    # Create agent_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            message TEXT,
            level TEXT DEFAULT 'info',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize database
init_db()

# WebSocket manager
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Initialize WebSocket manager
ws_manager = WebSocketManager()

# Security utilities
def hash_password(password: str) -> str:
    """Hash a password for storing."""
    salt = secrets.token_hex(16)
    return f"{salt}${hashlib.sha256(salt.encode() + password.encode()).hexdigest()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    salt, hashed = stored_password.split("$")
    return hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest() == hashed

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectUpdate(BaseModel):
    name: str
    description: str
    status: str

class AgentStatus(BaseModel):
    agent_name: str
    status: str
    message: str

# Security dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Get user from database
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, email, full_name, is_active, is_admin
        FROM users
        WHERE username = ?
    ''', (token_data.username,))

    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise credentials_exception

    return User(
        id=user[0],
        username=user[1],
        email=user[2],
        full_name=user[3],
        is_active=user[4],
        is_admin=user[5]
    )

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# API Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    # Get user from database
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, email, hashed_password, full_name, is_active, is_admin
        FROM users
        WHERE username = ?
    ''', (form_data.username,))

    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(user[3], form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[1]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, current_user: User = Depends(get_admin_user)):
    """Create a new user (admin only)"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute('''
        SELECT id FROM users WHERE username = ? OR email = ?
    ''', (user.username, user.email))

    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    # Create user
    hashed_password = hash_password(user.password)
    cursor.execute('''
        INSERT INTO users (username, email, hashed_password, full_name)
        VALUES (?, ?, ?, ?)
    ''', (user.username, user.email, hashed_password, user.full_name))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Get created user
    created_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
        is_admin=False
    )

    return created_user

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user

@app.get("/users/", response_model=List[User])
async def get_users(current_user: User = Depends(get_admin_user)):
    """Get all users (admin only)"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, email, full_name, is_active, is_admin
        FROM users
    ''')

    users = []
    for row in cursor.fetchall():
        users.append(User(
            id=row[0],
            username=row[1],
            email=row[2],
            full_name=row[3],
            is_active=row[4],
            is_admin=row[5]
        ))

    conn.close()
    return users

@app.post("/projects/", response_model=dict)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new project"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO projects (name, description, owner_id)
        VALUES (?, ?, ?)
    ''', (project.name, project.description, current_user.id))

    project_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Broadcast project creation
    await ws_manager.broadcast(json.dumps({
        "event": "project_created",
        "project_id": project_id,
        "project_name": project.name
    }))

    return {"message": "Project created successfully", "project_id": project_id}

@app.get("/projects/", response_model=dict)
async def get_projects(current_user: User = Depends(get_current_active_user)):
    """Get all projects for current user"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Get projects owned by user or where user is a collaborator
    cursor.execute('''
        SELECT id, name, description, status, created_at, updated_at
        FROM projects
        WHERE owner_id = ?
    ''', (current_user.id,))

    projects = []
    for row in cursor.fetchall():
        projects.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        })

    conn.close()
    return {"projects": projects}

@app.post("/projects/{project_id}/agents/", response_model=dict)
async def execute_agent(
    project_id: int,
    agent_name: str,
    current_user: User = Depends(get_current_active_user)
):
    """Execute an agent for a project"""
    # Get project from database
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT name, description, status, owner_id
        FROM projects
        WHERE id = ?
    ''', (project_id,))

    project = cursor.fetchone()
    if not project:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user has access to the project
    if project[3] != current_user.id:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    # Create agent record
    cursor.execute('''
        INSERT INTO agents (project_id, name, status)
        VALUES (?, ?, ?)
    ''', (project_id, agent_name, "running"))

    agent_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Execute agent
    try:
        # Create role coordinator
        coordinator = RoleCoordinator(
            use_unified_roles=True,
            use_task_decomposer=True,
            use_reviewer=True,
            use_full_workflow=True,
            use_test_runner=True,
            use_agent_monitor=True
        )

        # Execute agent
        result = await coordinator.run_workflow({
            "requirements": f"Execute {agent_name} for project {project[0]}",
            "project_name": project[0],
            "project_description": project[1]
        })

        # Update agent status
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE agents
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', ("completed", agent_id))

        conn.commit()
        conn.close()

        # Broadcast agent completion
        await ws_manager.broadcast(json.dumps({
            "event": "agent_completed",
            "agent_id": agent_id,
            "agent_name": agent_name,
            "status": "completed"
        }))

        return {"message": "Agent executed successfully", "result": result}

    except Exception as e:
        # Update agent status
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE agents
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', ("failed", agent_id))

        conn.commit()
        conn.close()

        # Broadcast agent failure
        await ws_manager.broadcast(json.dumps({
            "event": "agent_failed",
            "agent_id": agent_id,
            "agent_name": agent_name,
            "error": str(e)
        }))

        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects/{project_id}/agents/", response_model=dict)
async def get_project_agents(
    project_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get agents for a project"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Check if user has access to the project
    cursor.execute('''
        SELECT owner_id FROM projects WHERE id = ?
    ''', (project_id,))

    project = cursor.fetchone()
    if not project or project[0] != current_user.id:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    cursor.execute('''
        SELECT id, name, status, created_at, updated_at
        FROM agents
        WHERE project_id = ?
    ''', (project_id,))

    agents = []
    for row in cursor.fetchall():
        agents.append({
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "created_at": row[3],
            "updated_at": row[4]
        })

    conn.close()
    return {"agents": agents}

@app.get("/agents/{agent_id}/logs/", response_model=dict)
async def get_agent_logs(
    agent_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get logs for an agent"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Check if user has access to the agent
    cursor.execute('''
        SELECT p.owner_id
        FROM agents a
        JOIN projects p ON a.project_id = p.id
        WHERE a.id = ?
    ''', (agent_id,))

    owner = cursor.fetchone()
    if not owner or owner[0] != current_user.id:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to access this agent")

    cursor.execute('''
        SELECT message, level, timestamp
        FROM agent_logs
        WHERE agent_id = ?
        ORDER BY timestamp DESC
    ''', (agent_id,))

    logs = []
    for row in cursor.fetchall():
        logs.append({
            "message": row[0],
            "level": row[1],
            "timestamp": row[2]
        })

    conn.close()
    return {"logs": logs}

# WebSocket Endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket)

    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(10)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)












