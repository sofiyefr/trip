import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001/api',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
});

// Add a request interceptor to add the token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // Validate token before adding to request
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length !== 3) {
          // Invalid token format, remove it
          console.error('Invalid token format');
          localStorage.removeItem('token');
          window.location.href = '/login';
          return Promise.reject('Invalid token format');
        }
        
        // Try to parse the token payload
        try {
          const payload = JSON.parse(atob(tokenParts[1]));
          const expirationTime = payload.exp * 1000;
          
          if (Date.now() >= expirationTime) {
            // Token has expired, remove it
            console.error('Token has expired');
            localStorage.removeItem('token');
            window.location.href = '/login';
            return Promise.reject('Token expired');
          }
        } catch (parseError) {
          console.error('Failed to parse token payload:', parseError);
          localStorage.removeItem('token');
          window.location.href = '/login';
          return Promise.reject('Invalid token content');
        }
        
        config.headers.Authorization = `Bearer ${token}`;
      } catch (error) {
        // Token parsing error, remove it
        console.error('Token validation error:', error);
        localStorage.removeItem('token');
        window.location.href = '/login';
        return Promise.reject('Token parsing error');
      }
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.status, error.message);
    
    // Handle different error types
    if (error.response) {
      // Server responded with a status code outside of 2xx range
      console.log('Response data:', error.response.data);
      console.log('Response status:', error.response.status);
      
      // Handle authentication errors
      if (error.response.status === 401 || error.response.status === 422) {
        const errorData = error.response.data;
        if (
          errorData?.error === 'Invalid token' || 
          errorData?.error === 'Token expired' ||
          errorData?.error === 'Authentication error' ||
          errorData?.message?.includes('Subject') ||
          errorData?.message?.includes('token')
        ) {
          console.error('Authentication error:', errorData?.message);
          localStorage.removeItem('token');
          // Add a small delay before redirect to allow error logging
          setTimeout(() => {
            window.location.href = '/login';
          }, 100);
        }
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.log('No response received:', error.request);
    } else {
      // Something happened in setting up the request
      console.log('Error setting up request:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api; 