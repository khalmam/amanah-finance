// Authentication utility functions for JWT token management

/**
 * Get access token from localStorage
 */
export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

/**
 * Get refresh token from localStorage
 */
export const getRefreshToken = () => {
  return localStorage.getItem('refresh_token');
};

/**
 * Store authentication tokens
 */
export const setTokens = (accessToken, refreshToken) => {
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
};

/**
 * Clear all authentication tokens
 */
export const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return !!getAccessToken();
};

/**
 * Make authenticated API request with automatic token refresh
 */
export const authenticatedFetch = async (url, options = {}) => {
  const accessToken = getAccessToken();
  
  if (!accessToken) {
    throw new Error('No access token available');
  }

  // Add Authorization header
  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  };

  try {
    let response = await fetch(url, {
      ...options,
      headers,
    });

    // If token expired, try to refresh
    if (response.status === 401) {
      const refreshToken = getRefreshToken();
      
      if (!refreshToken) {
        clearTokens();
        window.location.href = '/login';
        throw new Error('Session expired');
      }

      // Attempt to refresh token
      const refreshResponse = await fetch('/api/auth/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (refreshResponse.ok) {
        const data = await refreshResponse.json();
        setTokens(data.access, refreshToken);

        // Retry original request with new token
        headers.Authorization = `Bearer ${data.access}`;
        response = await fetch(url, {
          ...options,
          headers,
        });
      } else {
        // Refresh failed, logout user
        clearTokens();
        window.location.href = '/login';
        throw new Error('Session expired');
      }
    }

    return response;
  } catch (error) {
    console.error('Authenticated fetch error:', error);
    throw error;
  }
};

/**
 * Logout user
 */
export const logout = () => {
  clearTokens();
  window.location.href = '/login';
};
