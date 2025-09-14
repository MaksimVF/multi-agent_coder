
















import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from '../../web_ui/src/App';
import axios from 'axios';

// Mock axios
jest.mock('axios');

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();

    // Mock localStorage
    localStorage.clear();
    jest.spyOn(localStorage, 'getItem').mockReturnValue(null);
  });

  test('renders login button when not authenticated', () => {
    render(<App />);
    expect(screen.getByText('Login')).toBeInTheDocument();
  });

  test('shows login prompt when not authenticated', () => {
    render(<App />);
    expect(screen.getByText('Please login to access the system')).toBeInTheDocument();
  });

  test('shows user info when authenticated', async () => {
    // Mock token in localStorage
    localStorage.setItem('token', 'fake-token');

    // Mock API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/users/me/') {
        return Promise.resolve({
          data: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            full_name: 'Test User',
            is_active: true,
            is_admin: false
          }
        });
      }
      if (url === 'http://localhost:8000/projects/') {
        return Promise.resolve({
          data: {
            projects: []
          }
        });
      }
      return Promise.reject(new Error('not found'));
    });

    render(<App />);

    // Wait for API calls to complete
    await screen.findByText('Logged in as: testuser');

    expect(screen.getByText('Logged in as: testuser')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  test('allows logout', async () => {
    // Mock token in localStorage
    localStorage.setItem('token', 'fake-token');

    // Mock API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/users/me/') {
        return Promise.resolve({
          data: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            full_name: 'Test User',
            is_active: true,
            is_admin: false
          }
        });
      }
      if (url === 'http://localhost:8000/projects/') {
        return Promise.resolve({
          data: {
            projects: []
          }
        });
      }
      return Promise.reject(new Error('not found'));
    });

    render(<App />);

    // Wait for API calls to complete
    await screen.findByText('Logged in as: testuser');

    // Click logout
    fireEvent.click(screen.getByText('Logout'));

    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Please login to access the system')).toBeInTheDocument();
  });

  test('shows projects when authenticated', async () => {
    // Mock token in localStorage
    localStorage.setItem('token', 'fake-token');

    // Mock API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/users/me/') {
        return Promise.resolve({
          data: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            full_name: 'Test User',
            is_active: true,
            is_admin: false
          }
        });
      }
      if (url === 'http://localhost:8000/projects/') {
        return Promise.resolve({
          data: {
            projects: [
              { id: 1, name: 'Project 1', description: 'Description 1', status: 'pending' },
              { id: 2, name: 'Project 2', description: 'Description 2', status: 'completed' }
            ]
          }
        });
      }
      return Promise.reject(new Error('not found'));
    });

    render(<App />);

    // Wait for API calls to complete
    await screen.findByText('Project 1');

    expect(screen.getByText('Project 1')).toBeInTheDocument();
    expect(screen.getByText('Project 2')).toBeInTheDocument();
  });

  test('shows admin interface for admin users', async () => {
    // Mock token in localStorage
    localStorage.setItem('token', 'fake-token');

    // Mock API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/users/me/') {
        return Promise.resolve({
          data: {
            id: 1,
            username: 'admin',
            email: 'admin@example.com',
            full_name: 'Admin User',
            is_active: true,
            is_admin: true
          }
        });
      }
      if (url === 'http://localhost:8000/projects/') {
        return Promise.resolve({
          data: {
            projects: []
          }
        });
      }
      return Promise.reject(new Error('not found'));
    });

    render(<App />);

    // Wait for API calls to complete
    await screen.findByText('System Logs');

    expect(screen.getByText('System Logs')).toBeInTheDocument();
    expect(screen.getByText('All Reports')).toBeInTheDocument();
  });

  test('allows project creation', async () => {
    // Mock token in localStorage
    localStorage.setItem('token', 'fake-token');

    // Mock API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/users/me/') {
        return Promise.resolve({
          data: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            full_name: 'Test User',
            is_active: true,
            is_admin: false
          }
        });
      }
      if (url === 'http://localhost:8000/projects/') {
        return Promise.resolve({
          data: {
            projects: []
          }
        });
      }
      return Promise.reject(new Error('not found'));
    });

    axios.post.mockImplementation((url, data) => {
      if (url === 'http://localhost:8000/projects/') {
        return Promise.resolve({
          data: {
            message: 'Project created successfully',
            project_id: 1
          }
        });
      }
      return Promise.reject(new Error('not found'));
    });

    render(<App />);

    // Wait for API calls to complete
    await screen.findByText('Create Project');

    // Mock prompt
    window.prompt = jest.fn()
      .mockReturnValueOnce('New Project')
      .mockReturnValueOnce('Project Description');

    // Click create project
    fireEvent.click(screen.getByText('Create Project'));

    // Wait for API call to complete
    await new Promise(resolve => setTimeout(resolve, 100));

    expect(axios.post).toHaveBeenCalledWith(
      'http://localhost:8000/projects/',
      {
        name: 'New Project',
        description: 'Project Description'
      },
      expect.any(Object)
    );
  });
});
















