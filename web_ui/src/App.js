














import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [projects, setProjects] = useState([]);
  const [agents, setAgents] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [ws, setWs] = useState(null);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  // Initialize axios with token
  const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
      'Authorization': token ? `Bearer ${token}` : ''
    }
  });

  // Connect to WebSocket
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket message:', data);

      // Handle different events
      switch (data.event) {
        case 'project_created':
          fetchProjects();
          break;
        case 'agent_completed':
        case 'agent_failed':
          if (selectedProject) {
            fetchProjectAgents(selectedProject.id);
          }
          break;
        default:
          break;
      }
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, [selectedProject]);

  // Fetch user info on mount
  useEffect(() => {
    if (token) {
      fetchUser();
      fetchProjects();
    }
  }, [token]);

  // Fetch user info
  const fetchUser = async () => {
    try {
      const response = await api.get('/users/me/');
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user:', error);
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
    }
  };

  // Fetch projects
  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects/');
      setProjects(response.data.projects);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  // Fetch agents for selected project
  const fetchProjectAgents = async (projectId) => {
    try {
      const response = await api.get(`/projects/${projectId}/agents/`);
      setAgents(response.data.agents);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  // Login
  const login = async () => {
    const username = prompt('Enter username:');
    const password = prompt('Enter password:');

    if (username && password) {
      try {
        const response = await axios.post('http://localhost:8000/token', {
          username,
          password
        }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });

        const token = response.data.access_token;
        setToken(token);
        localStorage.setItem('token', token);
        api.defaults.headers['Authorization'] = `Bearer ${token}`;
        fetchUser();
        fetchProjects();
      } catch (error) {
        console.error('Error logging in:', error);
        alert('Login failed. Please check your credentials.');
      }
    }
  };

  // Logout
  const logout = () => {
    setUser(null);
    setToken(null);
    setProjects([]);
    setAgents([]);
    setSelectedProject(null);
    localStorage.removeItem('token');
    delete api.defaults.headers['Authorization'];
  };

  // Create project
  const createProject = async () => {
    const name = prompt('Enter project name:');
    const description = prompt('Enter project description:');

    if (name && description) {
      try {
        await api.post('/projects/', {
          name,
          description
        });
        fetchProjects();
      } catch (error) {
        console.error('Error creating project:', error);
      }
    }
  };

  // Execute agent
  const executeAgent = async (agentName) => {
    if (selectedProject) {
      try {
        await api.post(`/projects/${selectedProject.id}/agents/`, null, {
          params: { agent_name: agentName }
        });
        fetchProjectAgents(selectedProject.id);
      } catch (error) {
        console.error('Error executing agent:', error);
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Multi-Agent Coder</h1>
        {user ? (
          <div className="user-info">
            <span>Logged in as: {user.username}</span>
            <button onClick={logout}>Logout</button>
          </div>
        ) : (
          <button onClick={login}>Login</button>
        )}
      </header>

      {user ? (
        <div className="content">
          <div className="projects">
            <h2>Projects</h2>
            <button onClick={createProject}>Create Project</button>
            <ul>
              {projects.map(project => (
                <li
                  key={project.id}
                  onClick={() => {
                    setSelectedProject(project);
                    fetchProjectAgents(project.id);
                  }}
                  className={selectedProject && selectedProject.id === project.id ? 'selected' : ''}
                >
                  {project.name}
                </li>
              ))}
            </ul>
          </div>

          {selectedProject && (
            <div className="project-details">
              <h2>{selectedProject.name}</h2>
              <p>{selectedProject.description}</p>
              <p>Status: {selectedProject.status}</p>

              <div className="agents">
                <h3>Agents</h3>
                <button onClick={() => executeAgent('ProjectManager')}>Run ProjectManager</button>
                <button onClick={() => executeAgent('AnalystArchitect')}>Run AnalystArchitect</button>
                <button onClick={() => executeAgent('DeveloperEngineer')}>Run DeveloperEngineer</button>
                <button onClick={() => executeAgent('TesterQa')}>Run TesterQa</button>

                <ul>
                  {agents.map(agent => (
                    <li key={agent.id}>
                      {agent.name} - {agent.status}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="login-prompt">
          <p>Please login to access the system</p>
        </div>
      )}
    </div>
  );
}

export default App;














