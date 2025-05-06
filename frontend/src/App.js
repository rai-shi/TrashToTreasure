import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './App.css';

// Layout components
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Auth components
import Login from './components/auth/Login';
import Register from './components/auth/Register';

// Page components
import Home from './pages/Home';
import Profile from './pages/Profile';
import Explore from './pages/Explore';
import NewProject from './pages/NewProject';
import ProjectDetail from './pages/ProjectDetail';

function App() {
  // Basit auth kontrol fonksiyonu - ileride JWT token kontrolü ile geliştirilecek
  const isAuthenticated = () => {
    return localStorage.getItem('access_token') !== null;
  };

  // Protected route için özel component
  const ProtectedRoute = ({ children }) => {
    if (!isAuthenticated()) {
      return <Navigate to="/login" replace />;
    }
    return children;
  };

  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              } 
            />
            <Route path="/explore" element={<Explore />} />
            <Route 
              path="/project/new" 
              element={
                <ProtectedRoute>
                  <NewProject />
                </ProtectedRoute>
              } 
            />
            <Route path="/project/:id" element={<ProjectDetail />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
