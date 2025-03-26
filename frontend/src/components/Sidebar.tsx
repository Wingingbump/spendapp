import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  FiGrid, 
  FiPieChart, 
  FiDollarSign, 
  FiTrendingUp, 
  FiFileText, 
  FiSettings, 
  FiHelpCircle,
  FiLogOut
} from 'react-icons/fi';
import { useAuth } from '../contexts/AuthContext';

interface SidebarProps {
  isCollapsed: boolean;
  onCollapse: (collapsed: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, onCollapse }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { icon: FiGrid, label: 'Dashboard', path: '/dashboard' },
    { icon: FiFileText, label: 'Transactions', path: '/transactions' },
    { icon: FiDollarSign, label: 'Budget', path: '/budget' },
    { icon: FiPieChart, label: 'Analytics', path: '/analytics' },
    { icon: FiSettings, label: 'Settings', path: '/settings' },
  ];

  return (
    <div 
      className={`fixed top-16 left-0 h-[calc(100vh-4rem)] bg-emerald-900 text-white transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
    >
      <nav className="h-full flex flex-col">
        <ul className="flex-1 space-y-2 px-3 pt-3">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                    isActive 
                      ? 'bg-emerald-800/50 text-emerald-300' 
                      : 'hover:bg-emerald-800/30'
                  }`}
                  title={isCollapsed ? item.label : undefined}
                >
                  <div className="w-5 h-5 flex items-center justify-center flex-shrink-0">
                    <Icon size={20} />
                  </div>
                  {!isCollapsed && <span className="ml-3">{item.label}</span>}
                </Link>
              </li>
            );
          })}
          <li>
            <button
              onClick={() => onCollapse(!isCollapsed)}
              className={`flex items-center px-4 py-3 rounded-lg hover:bg-emerald-800/30 transition-colors w-full ${
                isCollapsed ? 'justify-center' : ''
              }`}
              title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              <div className="w-5 h-5 flex items-center justify-center flex-shrink-0">
                <FiSettings 
                  size={20} 
                  className={`transform transition-transform ${isCollapsed ? 'rotate-180' : '-rotate-90'}`}
                />
              </div>
            </button>
          </li>
        </ul>

        <div className="px-3 pb-6">
          {!isCollapsed && (
            <div className="bg-emerald-800/50 rounded-lg p-4 mb-4">
              <h3 className="font-medium mb-2">Have a question?</h3>
              <p className="text-sm text-emerald-200/90 mb-3">
                Send us a message and we will get back to you in no time.
              </p>
              <button className="flex items-center space-x-2 text-sm text-emerald-300 hover:text-emerald-200">
                <div className="w-4 h-4 flex items-center justify-center flex-shrink-0">
                  <FiHelpCircle size={16} />
                </div>
                <span>Contact us</span>
              </button>
            </div>
          )}

          <button
            onClick={handleLogout}
            className={`flex items-center rounded-lg hover:bg-emerald-800/30 transition-colors w-full ${
              isCollapsed ? 'justify-center py-3' : 'space-x-3 px-4 py-3'
            }`}
            title={isCollapsed ? 'Log out' : undefined}
          >
            <div className="w-5 h-5 flex items-center justify-center flex-shrink-0">
              <FiLogOut size={20} />
            </div>
            {!isCollapsed && <span>Log out</span>}
          </button>
        </div>
      </nav>
    </div>
  );
};

export default Sidebar; 