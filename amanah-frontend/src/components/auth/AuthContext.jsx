import React, { createContext, useState, useContext, useEffect } from 'react';
import { isAuthenticated, clearTokens } from '/src/utils/authUtils';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuth, setIsAuth] = useState(isAuthenticated());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status on mount
    setIsAuth(isAuthenticated());
    setLoading(false);
  }, []);

  const login = (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    setIsAuth(true);
  };

  const logout = () => {
    clearTokens();
    setIsAuth(false);
    window.location.href = '/login';
  };

  const value = {
    isAuth,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
