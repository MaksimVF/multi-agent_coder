












import os
import json
import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

# Models
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

# API Endpoints
@app.post("/projects/")
async def create_project(project: ProjectCreate):
    """Create a new project"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO projects (name, description)
        VALUES (?, ?)
    ''', (project.name, project.description))

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

@app.get("/projects/")
async def get_projects():
    """Get all projects"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, description, status, created_at, updated_at
        FROM projects
    ''')

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

@app.post("/projects/{project_id}/agents/")
async def execute_agent(project_id: int, agent_name: str):
    """Execute an agent for a project"""
    # Get project from database
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT name, description, status
        FROM projects
        WHERE id = ?
    ''', (project_id,))

    project = cursor.fetchone()
    if not project:
        conn.close()
        return {"error": "Project not found"}, 404

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

        return {"error": str(e)}, 500

@app.get("/projects/{project_id}/agents/")
async def get_project_agents(project_id: int):
    """Get agents for a project"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

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

@app.get("/agents/{agent_id}/logs/")
async def get_agent_logs(agent_id: int):
    """Get logs for an agent"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

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












