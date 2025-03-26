import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSearch, FiBell, FiUser } from 'react-icons/fi';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-emerald-900 text-white shadow-md z-50">
      <div className="h-full px-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-semibold">SpendApp</h1>
        </div>

        <div className="flex items-center space-x-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search..."
              className="bg-emerald-800/50 text-white placeholder-emerald-200/70 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <FiSearch className="absolute right-3 top-1/2 transform -translate-y-1/2 text-emerald-200/70" />
          </div>

          <button className="p-2 hover:bg-emerald-800/50 rounded-lg transition-colors">
            <FiBell className="w-5 h-5" />
          </button>

          <button 
            onClick={handleLogout}
            className="p-2 hover:bg-emerald-800/50 rounded-lg transition-colors"
          >
            <div className="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center">
              <FiUser className="w-5 h-5" />
            </div>
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 