import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
// 1. Import the provider
import { AuthProvider } from './components/auth/AuthContext' 

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* 2. Wrap App so every route can use useAuth() */}
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>,
)