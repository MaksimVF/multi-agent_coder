














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

  // Fetch agent logs
  const fetchAgentLogs = async (agentId) => {
    try {
      const response = await api.get(`/agents/${agentId}/logs/`);
      setAgentLogs(response.data.logs);
    } catch (error) {
      console.error('Error fetching agent logs:', error);
    }
  };

  // Fetch agent reports
  const fetchAgentReports = async (agentId) => {
    try {
      const response = await api.get(`/agents/${agentId}/reports/`);
      setAgentReports(response.data.reports);
    } catch (error) {
      console.error('Error fetching agent reports:', error);
    }
  };

  // Fetch system logs (admin only)
  const fetchSystemLogs = async () => {
    try {
      const response = await api.get('/admin/logs/');
      setSystemLogs(response.data.logs);
    } catch (error) {
      console.error('Error fetching system logs:', error);
    }
  };

  // Fetch all reports (admin only)
  const fetchAllReports = async () => {
    try {
      const response = await api.get('/admin/reports/');
      setAllReports(response.data.reports);
    } catch (error) {
      console.error('Error fetching all reports:', error);
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
    setSelectedAgent(null);
    setAgentLogs([]);
    setAgentReports([]);
    setSystemLogs([]);
    setAllReports([]);
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
          <nav className="sidebar">
            <h3>Navigation</h3>
            <ul>
              <li onClick={() => setView('projects')}>Projects</li>
              {user.is_admin && (
                <>
                  <li onClick={() => setView('logs')}>System Logs</li>
                  <li onClick={() => setView('reports')}>All Reports</li>
                </>
              )}
            </ul>
          </nav>

          <div className="main-content">
            {view === 'projects' && (
              <>
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
                          <li
                            key={agent.id}
                            onClick={() => {
                              setSelectedAgent(agent);
                              fetchAgentLogs(agent.id);
                              fetchAgentReports(agent.id);
                            }}
                            className={selectedAgent && selectedAgent.id === agent.id ? 'selected' : ''}
                          >
                            {agent.name} - {agent.status}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {selectedAgent && (
                      <div className="agent-details">
                        <h3>Agent Details: {selectedAgent.name}</h3>
                        <p>Status: {selectedAgent.status}</p>

                        <div className="agent-logs">
                          <h4>Logs</h4>
                          <ul>
                            {agentLogs.map((log, index) => (
                              <li key={index}>
                                <strong>{log.timestamp}</strong> [{log.level}]: {log.message}
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div className="agent-reports">
                          <h4>Reports</h4>
                          <ul>
                            {agentReports.map((report, index) => (
                              <li key={index}>
                                <strong>{report.report_type}</strong> ({report.created_at}):<br/>
                                <pre>{JSON.stringify(report.data, null, 2)}</pre>
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
                <button onClick={fetchSystemLogs}>Refresh Logs</button>
                <ul>
                  {systemLogs.map(log => (
                    <li key={log.id}>
                      <strong>{log.timestamp}</strong> [{log.level}]: {log.action} - {log.details}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {view === 'reports' && user.is_admin && (
              <div className="all-reports">
                <h2>All Reports</h2>
                <button onClick={fetchAllReports}>Refresh Reports</button>
                <ul>
                  {allReports.map(report => (
                    <li key={report.id}>
                      <strong>{report.created_at}</strong> - {report.report_type} for {report.agent_name} in {report.project_name}<br/>
                      <pre>{JSON.stringify(report.data, null, 2)}</pre>
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














