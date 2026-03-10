import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/auth/login";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import RegisterChoice from "./components/auth/RegisterChoice";
import RegisterInvestor from "./components/auth/RegisterInvestor";
import RegisterEntrepreneur from "./components/auth/RegisterEntrepreneur";


// const Dashboard = () => <h1>Dashboard</h1>;

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />
        <Route path="/register" 
        element={<RegisterChoice />} />
        
        <Route path="/register/investor" 
        element={<RegisterInvestor />} />
        <Route path="/register/entrepreneur" 
        element={<RegisterEntrepreneur />} />

        <Route path="*" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;