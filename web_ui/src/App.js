














import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [projects, setProjects] = useState([]);
  const [agents, setAgents] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [ws, setWs] = useState(null);

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

  // Fetch projects
  const fetchProjects = async () => {
    try {
      const response = await axios.get('http://localhost:8000/projects/');
      setProjects(response.data.projects);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  // Fetch agents for selected project
  const fetchProjectAgents = async (projectId) => {
    try {
      const response = await axios.get(`http://localhost:8000/projects/${projectId}/agents/`);
      setAgents(response.data.agents);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  // Create project
  const createProject = async () => {
    const name = prompt('Enter project name:');
    const description = prompt('Enter project description:');

    if (name && description) {
      try {
        await axios.post('http://localhost:8000/projects/', {
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
        await axios.post(`http://localhost:8000/projects/${selectedProject.id}/agents/`, null, {
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
      </header>

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
    </div>
  );
}

export default App;














