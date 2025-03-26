import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import Transactions from './components/Transactions';
import Budget from './components/Budget';
import Analytics from './components/Analytics';
import Settings from './components/Settings';
import { useAuth } from './contexts/AuthContext';

const App: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { isAuthenticated } = useAuth();

  const mainContentClass = `flex-1 transition-all duration-300 ${isCollapsed ? 'ml-16' : 'ml-48'}`;

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route
            path="/login"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <LoginPage />
              )
            }
          />
          <Route
            path="/dashboard"
            element={
              isAuthenticated ? (
                <Layout>
                  <Sidebar isCollapsed={isCollapsed} onCollapse={setIsCollapsed} />
                  <div className={mainContentClass}>
                    <Dashboard />
                  </div>
                </Layout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/transactions"
            element={
              isAuthenticated ? (
                <Layout>
                  <Sidebar isCollapsed={isCollapsed} onCollapse={setIsCollapsed} />
                  <div className={mainContentClass}>
                    <Transactions />
                  </div>
                </Layout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/budget"
            element={
              isAuthenticated ? (
                <Layout>
                  <Sidebar isCollapsed={isCollapsed} onCollapse={setIsCollapsed} />
                  <div className={mainContentClass}>
                    <Budget />
                  </div>
                </Layout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/analytics"
            element={
              isAuthenticated ? (
                <Layout>
                  <Sidebar isCollapsed={isCollapsed} onCollapse={setIsCollapsed} />
                  <div className={mainContentClass}>
                    <Analytics />
                  </div>
                </Layout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/settings"
            element={
              isAuthenticated ? (
                <Layout>
                  <Sidebar isCollapsed={isCollapsed} onCollapse={setIsCollapsed} />
                  <div className={mainContentClass}>
                    <Settings />
                  </div>
                </Layout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App; 