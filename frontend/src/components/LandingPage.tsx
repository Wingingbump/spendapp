import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useTheme } from '../contexts/ThemeContext';

const LandingPage: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);

    // If authenticated, redirect to dashboard
    if (token) {
      navigate('/dashboard');
    }
  }, [navigate]);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center z-10"
        >
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
            Track Your Spending
            <span className="text-blue-600 dark:text-blue-400"> Smarter</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8">
            Connect your bank accounts and get insights into your spending habits
          </p>
          <div className="space-x-4">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link
                  to="/login?register=true"
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Get Started
                </Link>
                <Link
                  to="/login"
                  className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white px-8 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>
        </motion.div>
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 -z-10" />
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-16">
            Why Choose SpendApp?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="p-6 rounded-lg bg-gray-50 dark:bg-gray-800"
              >
                <div className="text-blue-600 dark:text-blue-400 text-4xl mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-16">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-blue-600 dark:bg-blue-400 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl">
                  {index + 1}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {step.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 dark:bg-blue-700">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-4xl font-bold text-white mb-8">
              Ready to Take Control of Your Finances?
            </h2>
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors inline-block"
              >
                Go to Dashboard
              </Link>
            ) : (
              <Link
                to="/login?register=true"
                className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors inline-block"
              >
                Start Free Trial
              </Link>
            )}
          </motion.div>
        </div>
      </section>

      {/* Theme Toggle Button */}
      <button
        onClick={toggleTheme}
        className="fixed bottom-8 right-8 p-3 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      >
        {theme === 'light' ? '🌙' : '☀️'}
      </button>
    </div>
  );
};

const features = [
  {
    icon: '📊',
    title: 'Smart Analytics',
    description: 'Get detailed insights into your spending patterns and financial health.',
  },
  {
    icon: '🔒',
    title: 'Secure Connection',
    description: 'Bank-level security with Plaid integration for safe account connections.',
  },
  {
    icon: '🎯',
    title: 'Budget Goals',
    description: 'Set and track your financial goals with personalized recommendations.',
  },
];

const steps = [
  {
    title: 'Sign Up',
    description: 'Create your account in seconds with just your email.',
  },
  {
    title: 'Connect Bank',
    description: 'Securely link your bank accounts using Plaid.',
  },
  {
    title: 'Track Spending',
    description: 'View your transactions and spending patterns.',
  },
  {
    title: 'Get Insights',
    description: 'Receive personalized recommendations and insights.',
  },
];

export default LandingPage; 