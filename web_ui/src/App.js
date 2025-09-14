














import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [projects, setProjects] = useState([]);
  const [agents, setAgents] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agentLogs, setAgentLogs] = useState([]);
  const [agentReports, setAgentReports] = useState([]);
  const [systemLogs, setSystemLogs] = useState([]);
  const [allReports, setAllReports] = useState([]);
  const [ws, setWs] = useState(null);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [view, setView] = useState('projects'); // 'projects', 'logs', 'reports'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);

  // Initialize axios with token
  const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
      'Authorization': token ? `Bearer ${token}` : ''
    }
  });

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => {
      setNotification(null);
    }, 5000);
  };

  // Connect to WebSocket
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
      console.log('WebSocket connected');
      showNotification('Connected to real-time updates', 'success');
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket message:', data);

      // Handle different events
      switch (data.event) {
        case 'project_created':
          fetchProjects();
          showNotification('New project created', 'info');
          break;
        case 'agent_completed':
          if (selectedProject) {
            fetchProjectAgents(selectedProject.id);
          }
          showNotification(`Agent ${data.agent_name} completed`, 'success');
          break;
        case 'agent_failed':
          if (selectedProject) {
            fetchProjectAgents(selectedProject.id);
          }
          showNotification(`Agent ${data.agent_name} failed: ${data.error}`, 'error');
          break;
        case 'system_log':
          if (view === 'logs') {
            fetchSystemLogs();
          }
          break;
        default:
          break;
      }
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
      showNotification('Disconnected from real-time updates', 'warning');
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, [selectedProject, view]);

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
      setLoading(true);
      const response = await api.get('/users/me/');
      setUser(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching user:', error);
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      setLoading(false);
    }
  };

  // Fetch projects
  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await api.get('/projects/');
      setProjects(response.data.projects);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching projects:', error);
      setError('Failed to fetch projects');
      setLoading(false);
    }
  };

  // Fetch agents for selected project
  const fetchProjectAgents = async (projectId) => {
    try {
      setLoading(true);
      const response = await api.get(`/projects/${projectId}/agents/`);
      setAgents(response.data.agents);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching agents:', error);
      setError('Failed to fetch agents');
      setLoading(false);
    }
  };

  // Fetch agent logs
  const fetchAgentLogs = async (agentId) => {
    try {
      setLoading(true);
      const response = await api.get(`/agents/${agentId}/logs/`);
      setAgentLogs(response.data.logs);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching agent logs:', error);
      setError('Failed to fetch agent logs');
      setLoading(false);
    }
  };

  // Fetch agent reports
  const fetchAgentReports = async (agentId) => {
    try {
      setLoading(true);
      const response = await api.get(`/agents/${agentId}/reports/`);
      setAgentReports(response.data.reports);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching agent reports:', error);
      setError('Failed to fetch agent reports');
      setLoading(false);
    }
  };

  // Fetch system logs (admin only)
  const fetchSystemLogs = async () => {
    try {
      setLoading(true);
      const response = await api.get('/admin/logs/');
      setSystemLogs(response.data.logs);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching system logs:', error);
      setError('Failed to fetch system logs');
      setLoading(false);
    }
  };

  // Fetch all reports (admin only)
  const fetchAllReports = async () => {
    try {
      setLoading(true);
      const response = await api.get('/admin/reports/');
      setAllReports(response.data.reports);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching all reports:', error);
      setError('Failed to fetch all reports');
      setLoading(false);
    }
  };

  // Login
  const login = async () => {
    const username = prompt('Enter username:');
    const password = prompt('Enter password:');

    if (username && password) {
      try {
        setLoading(true);
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
        showNotification('Login successful', 'success');
        setLoading(false);
      } catch (error) {
        console.error('Error logging in:', error);
        showNotification('Login failed. Please check your credentials.', 'error');
        setLoading(false);
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
    setSelectedAgent(null);
    setAgentLogs([]);
    setAgentReports([]);
    setSystemLogs([]);
    setAllReports([]);
    localStorage.removeItem('token');
    delete api.defaults.headers['Authorization'];
    showNotification('Logged out successfully', 'info');
  };

  // Create project
  const createProject = async () => {
    const name = prompt('Enter project name:');
    const description = prompt('Enter project description:');

    if (name && description) {
      try {
        setLoading(true);
        await api.post('/projects/', {
          name,
          description
        });
        fetchProjects();
        showNotification('Project created successfully', 'success');
        setLoading(false);
      } catch (error) {
        console.error('Error creating project:', error);
        showNotification('Failed to create project', 'error');
        setLoading(false);
      }
    }
  };

  // Execute agent
  const executeAgent = async (agentName) => {
    if (selectedProject) {
      try {
        setLoading(true);
        await api.post(`/projects/${selectedProject.id}/agents/`, null, {
          params: { agent_name: agentName }
        });
        fetchProjectAgents(selectedProject.id);
        showNotification(`Agent ${agentName} started`, 'info');
        setLoading(false);
      } catch (error) {
        console.error('Error executing agent:', error);
        showNotification(`Failed to start agent ${agentName}`, 'error');
        setLoading(false);
      }
    }
  };

  // Clear error
  const clearError = () => {
    setError(null);
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

      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
          <button onClick={() => setNotification(null)}>×</button>
        </div>
      )}

      {error && (
        <div className="error-banner">
          {error}
          <button onClick={clearError}>×</button>
        </div>
      )}

      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
        </div>
      )}

      {user ? (
        <div className="content">
          <nav className="sidebar">
            <h3>Navigation</h3>
            <ul>
              <li
                onClick={() => setView('projects')}
                className={view === 'projects' ? 'active' : ''}
              >
                Projects
              </li>
              {user.is_admin && (
                <>
                  <li
                    onClick={() => setView('logs')}
                    className={view === 'logs' ? 'active' : ''}
                  >
                    System Logs
                  </li>
                  <li
                    onClick={() => setView('reports')}
                    className={view === 'reports' ? 'active' : ''}
                  >
                    All Reports
                  </li>
                </>
              )}
            </ul>
          </nav>

          <div className="main-content">
            {view === 'projects' && (
              <>
                <div className="projects">
                  <h2>Projects</h2>
                  <button onClick={createProject} className="btn-primary">Create Project</button>
                  <ul className="project-list">
                    {projects.map(project => (
                      <li
                        key={project.id}
                        onClick={() => {
                          setSelectedProject(project);
                          fetchProjectAgents(project.id);
                        }}
                        className={selectedProject && selectedProject.id === project.id ? 'selected' : ''}
                      >
                        <div className="project-card">
                          <h3>{project.name}</h3>
                          <p>{project.description}</p>
                          <span className={`status ${project.status}`}>{project.status}</span>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>

                {selectedProject && (
                  <div className="project-details">
                    <h2>{selectedProject.name}</h2>
                    <p>{selectedProject.description}</p>
                    <p>Status: <span className={`status ${selectedProject.status}`}>{selectedProject.status}</span></p>

                    <div className="agents">
                      <h3>Agents</h3>
                      <div className="agent-buttons">
                        <button onClick={() => executeAgent('ProjectManager')} className="btn-secondary">Run ProjectManager</button>
                        <button onClick={() => executeAgent('AnalystArchitect')} className="btn-secondary">Run AnalystArchitect</button>
                        <button onClick={() => executeAgent('DeveloperEngineer')} className="btn-secondary">Run DeveloperEngineer</button>
                        <button onClick={() => executeAgent('TesterQa')} className="btn-secondary">Run TesterQa</button>
                      </div>

                      <ul className="agent-list">
                        {agents.map(agent => (
                          <li
                            key={agent.id}
                            onClick={() => {
                              setSelectedAgent(agent);
                              fetchAgentLogs(agent.id);
                              fetchAgentReports(agent.id);
                            }}
                            className={selectedAgent && selectedAgent.id === agent.id ? 'selected' : ''}
                          >
                            <div className="agent-card">
                              <h4>{agent.name}</h4>
                              <span className={`status ${agent.status}`}>{agent.status}</span>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {selectedAgent && (
                      <div className="agent-details">
                        <h3>Agent Details: {selectedAgent.name}</h3>
                        <p>Status: <span className={`status ${selectedAgent.status}`}>{selectedAgent.status}</span></p>

                        <div className="agent-logs">
                          <h4>Logs</h4>
                          <ul className="log-list">
                            {agentLogs.map((log, index) => (
                              <li key={index} className={`log-item ${log.level}`}>
                                <strong>{new Date(log.timestamp).toLocaleString()}</strong> [{log.level}]: {log.message}
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div className="agent-reports">
                          <h4>Reports</h4>
                          <ul className="report-list">
                            {agentReports.map((report, index) => (
                              <li key={index} className="report-item">
                                <div className="report-header">
                                  <strong>{report.report_type}</strong> ({new Date(report.created_at).toLocaleString()})
                                </div>
                                <pre className="report-data">{JSON.stringify(report.data, null, 2)}</pre>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}

            {view === 'logs' && user.is_admin && (
              <div className="system-logs">
                <h2>System Logs</h2>
                <button onClick={fetchSystemLogs} className="btn-primary">Refresh Logs</button>
                <ul className="log-list">
                  {systemLogs.map(log => (
                    <li key={log.id} className={`log-item ${log.level}`}>
                      <strong>{new Date(log.timestamp).toLocaleString()}</strong> [{log.level}]: {log.action} - {log.details}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {view === 'reports' && user.is_admin && (
              <div className="all-reports">
                <h2>All Reports</h2>
                <button onClick={fetchAllReports} className="btn-primary">Refresh Reports</button>
                <ul className="report-list">
                  {allReports.map(report => (
                    <li key={report.id} className="report-item">
                      <div className="report-header">
                        <strong>{new Date(report.created_at).toLocaleString()}</strong> - {report.report_type} for {report.agent_name} in {report.project_name}
                      </div>
                      <pre className="report-data">{JSON.stringify(report.data, null, 2)}</pre>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
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














