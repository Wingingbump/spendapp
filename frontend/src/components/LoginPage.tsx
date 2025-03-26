import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import { useAuth } from '../contexts/AuthContext';
import { FiUser, FiSettings } from 'react-icons/fi';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme } = useTheme();
  const { login } = useAuth();
  const isRegister = new URLSearchParams(location.search).get('register') === 'true';
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: isRegister ? '' : undefined,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isRegister ? '/register' : '/login';
      console.log('Attempting to login with:', { endpoint, email: formData.email });
      
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log('Login response:', data);

      if (!response.ok) {
        throw new Error(data.detail || 'An error occurred');
      }

      if (isRegister) {
        // After successful registration, log in automatically
        console.log('Registration successful, attempting login...');
        const loginResponse = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        });

        const loginData = await loginResponse.json();
        console.log('Auto-login response:', loginData);
        
        if (!loginResponse.ok) {
          throw new Error(loginData.detail || 'Login failed after registration');
        }

        login(loginData.access_token, loginData.user);
        console.log('Login successful, navigating to dashboard...');
        navigate('/dashboard');
      } else {
        login(data.access_token, data.user);
        console.log('Login successful, navigating to dashboard...');
        navigate('/dashboard');
      }
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col md:flex-row ${theme === 'dark' ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Left side - Illustration/Welcome */}
      <div className="hidden md:flex md:w-1/2 bg-emerald-900 text-white p-12 flex-col justify-between">
        <div>
          <h1 className="text-4xl font-bold mb-4">SpendWise</h1>
          <p className="text-emerald-200 text-lg">Take control of your finances with our smart expense tracking solution.</p>
        </div>
        <div className="space-y-6">
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center flex-shrink-0">
              <span>✓</span>
            </div>
            <p className="text-emerald-200">Track your expenses effortlessly</p>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center flex-shrink-0">
              <span>✓</span>
            </div>
            <p className="text-emerald-200">Get insights into your spending habits</p>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center flex-shrink-0">
              <span>✓</span>
            </div>
            <p className="text-emerald-200">Set and achieve financial goals</p>
          </div>
        </div>
      </div>

      {/* Right side - Login Form */}
      <div className={`flex-1 flex items-center justify-center p-8 ${theme === 'dark' ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              {isRegister ? 'Create your account' : 'Welcome back'}
            </h2>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
              <button
                onClick={() => navigate(isRegister ? '/login' : '/login?register=true')}
                className="font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-500"
              >
                {isRegister ? 'Sign in' : 'Sign up'}
              </button>
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {isRegister && (
              <div>
                <label htmlFor="full-name" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Full Name
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FiUser className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="full-name"
                    name="fullName"
                    type="text"
                    required
                    className="pl-10 w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                    placeholder="John Doe"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  />
                </div>
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Email address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiUser className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  className="pl-10 w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiSettings className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  className="pl-10 w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-sm p-3 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {loading ? 'Please wait...' : isRegister ? 'Create Account' : 'Sign in'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage; 