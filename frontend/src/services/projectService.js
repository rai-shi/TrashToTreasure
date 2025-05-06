import axios from 'axios';
import authService from './authService';
import geminiService from './geminiService';

const API_URL = 'http://localhost:8000';

// Create axios instance with authorization header
const authAxios = async () => {
  try {
    // Try to refresh token if needed
    const token = await authService.refreshToken();
    
    return axios.create({
      baseURL: API_URL,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    // If token refresh fails, create instance without auth header
    return axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
};

// Create axios instance for file uploads
const fileUploadAxios = async () => {
  try {
    // Try to refresh token if needed
    const token = await authService.refreshToken();
    
    return axios.create({
      baseURL: API_URL,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
  } catch (error) {
    return axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
};

const projectService = {
  /**
   * Get user's projects
   */
  getUserProjects: async () => {
    try {
      const axiosInstance = await authAxios();
      const response = await axiosInstance.get('/project/my-ideas');
      return response.data;
    } catch (error) {
      console.error('Error fetching user projects:', error);
      if (error.response?.status === 401) {
        authService.logout();
        throw new Error('Your session has expired. Please login again.');
      }
      throw error;
    }
  },

  /**
   * Create a new project with image and description
   */
  createProject: async (projectData, imageFile) => {
    try {
      // First, generate roadmap using Gemini
      console.log('[DEBUG] Generating roadmap with Gemini...');
      const roadmap = await geminiService.generateRoadmap(
        imageFile,
        projectData.name,
        projectData.description
      );
      console.log('[DEBUG] Generated roadmap:', roadmap);

      // Create FormData to send both text and file data
      const formData = new FormData();
      
      // Add fields directly to match FastAPI Form expectations
      formData.append('name', projectData.name);
      formData.append('description', projectData.description);
      formData.append('image', imageFile);
      formData.append('roadmap', JSON.stringify(roadmap));

      const axiosInstance = await fileUploadAxios();
      const response = await axiosInstance.post('/projects', formData);
      return response.data;
    } catch (error) {
      console.error('Error creating project:', error);
      if (error.response?.status === 401) {
        authService.logout();
        throw new Error('Your session has expired. Please login again.');
      }
      throw error;
    }
  },

  /**
   * Get project roadmap
   */
  getProjectRoadmap: (projectId, projects) => {
    try {
      // Projeler içinde projectId'yi bul ve ilgili yol haritasını döndür
      const project = projects.find(p => p.id === projectId);
      if (project && project.roadmap) {
        console.log('[DEBUG2] Found roadmap for project:', project.name);
        return project.roadmap;
      } else {
        throw new Error('Roadmap not found for this project.');
      }
    } catch (error) {
      console.error('Error retrieving roadmap from project:', error);
      throw new Error('Failed to fetch roadmap from project.');
    }
  }

};

export default projectService; 