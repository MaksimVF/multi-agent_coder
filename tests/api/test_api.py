















import pytest
import asyncio
import httpx
from fastapi.testclient import TestClient
from api_server import app, init_db, DATABASE_URL
import sqlite3
import os

# Initialize test database
@pytest.fixture(scope="module")
def test_db():
    """Create a test database"""
    # Create a temporary database
    test_db_url = "test_multi_agent_coder.db"

    # Remove if exists
    if os.path.exists(test_db_url):
        os.remove(test_db_url)

    # Initialize database
    conn = sqlite3.connect(test_db_url)
    cursor = conn.cursor()

    # Create tables
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            project_id INTEGER,
            report_type TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            level TEXT DEFAULT 'info',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

    yield test_db_url

    # Clean up
    if os.path.exists(test_db_url):
        os.remove(test_db_url)

@pytest.fixture(scope="module")
def client(test_db):
    """Create a test client"""
    # Override database URL
    import api_server
    api_server.DATABASE_URL = test_db

    # Initialize database
    init_db()

    # Create test client
    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
async def async_client(test_db):
    """Create an async test client"""
    # Override database URL
    import api_server
    api_server.DATABASE_URL = test_db

    # Initialize database
    init_db()

    # Create async client
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

def test_create_user(client):
    """Test user creation"""
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

def test_login(client):
    """Test user login"""
    # Create user first
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    # Login
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_project(client):
    """Test project creation"""
    # Create user and login
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Create project
    response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test project description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert data["message"] == "Project created successfully"

def test_get_projects(client):
    """Test getting projects"""
    # Create user and login
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Create project
    client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test project description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get projects
    response = client.get(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert len(data["projects"]) == 1
    assert data["projects"][0]["name"] == "Test Project"

def test_execute_agent(client):
    """Test agent execution"""
    # Create user and login
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Create project
    project_response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test project description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    project_id = project_response.json()["project_id"]

    # Execute agent
    response = client.post(
        f"/projects/{project_id}/agents/",
        params={"agent_name": "ProjectManager"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Agent executed successfully"

def test_get_agent_logs(client):
    """Test getting agent logs"""
    # Create user and login
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Create project
    project_response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test project description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    project_id = project_response.json()["project_id"]

    # Execute agent
    agent_response = client.post(
        f"/projects/{project_id}/agents/",
        params={"agent_name": "ProjectManager"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get agents
    agents_response = client.get(
        f"/projects/{project_id}/agents/",
        headers={"Authorization": f"Bearer {token}"}
    )

    agent_id = agents_response.json()["agents"][0]["id"]

    # Get agent logs
    response = client.get(
        f"/agents/{agent_id}/logs/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "logs" in data

def test_get_agent_reports(client):
    """Test getting agent reports"""
    # Create user and login
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )

    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Create project
    project_response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test project description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    project_id = project_response.json()["project_id"]

    # Execute agent
    agent_response = client.post(
        f"/projects/{project_id}/agents/",
        params={"agent_name": "ProjectManager"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get agents
    agents_response = client.get(
        f"/projects/{project_id}/agents/",
        headers={"Authorization": f"Bearer {token}"}
    )

    agent_id = agents_response.json()["agents"][0]["id"]

    # Get agent reports
    response = client.get(
        f"/agents/{agent_id}/reports/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "reports" in data

def test_admin_logs(client):
    """Test admin logs access"""
    # Create admin user and login
    client.post(
        "/users/",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpassword",
            "full_name": "Admin User"
        }
    )

    # Manually set admin flag in database
    conn = sqlite3.connect("test_multi_agent_coder.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET is_admin = TRUE
        WHERE username = 'admin'
    ''')
    conn.commit()
    conn.close()

    login_response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "adminpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Get system logs
    response = client.get(
        "/admin/logs/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "logs" in data

def test_admin_reports(client):
    """Test admin reports access"""
    # Create admin user and login
    client.post(
        "/users/",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpassword",
            "full_name": "Admin User"
        }
    )

    # Manually set admin flag in database
    conn = sqlite3.connect("test_multi_agent_coder.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET is_admin = TRUE
        WHERE username = 'admin'
    ''')
    conn.commit()
    conn.close()

    login_response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "adminpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token = login_response.json()["access_token"]

    # Get all reports
    response = client.get(
        "/admin/reports/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "reports" in data

if __name__ == "__main__":
    pytest.main()















