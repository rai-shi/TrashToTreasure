import axios from 'axios';

const API_URL = 'http://localhost:8002';

const authService = {
  getToken: () => {
    return localStorage.getItem('token');
  },

  setToken: (token) => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  },

  isTokenExpired: (token) => {
    if (!token) return true;
    
    try {
      // JWT tokens are base64 encoded. Split by dots and get the payload
      const payload = JSON.parse(atob(token.split('.')[1]));
      // Check if token is expired
      return payload.exp * 1000 < Date.now();
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true;
    }
  },

  refreshToken: async () => {
    try {
      const token = authService.getToken();
      
      if (!token) {
        throw new Error('No token found');
      }

      // Only try to refresh if token is expired
      if (authService.isTokenExpired(token)) {
        const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.data && response.data.access_token) {
          authService.setToken(response.data.access_token);
          return response.data.access_token;
        }
      }

      return token;
    } catch (error) {
      console.error('Error refreshing token:', error);
      authService.setToken(null);
      throw error;
    }
  },

  logout: () => {
    authService.setToken(null);
    // Add any other cleanup needed on logout
  }
};

export default authService; 