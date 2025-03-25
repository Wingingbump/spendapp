import React from 'react';
import { Link } from 'react-router-dom';
import { ChartBarIcon, CreditCardIcon, ArrowTrendingUpIcon } from '@heroicons/react/24/outline';

const features = [
  {
    name: 'Track Spending',
    description: 'Connect your bank accounts and track all your expenses in one place.',
    icon: CreditCardIcon,
  },
  {
    name: 'Analyze Trends',
    description: 'Get insights into your spending habits with detailed analytics.',
    icon: ChartBarIcon,
  },
  {
    name: 'Set Goals',
    description: 'Set and track financial goals to improve your saving habits.',
    icon: ArrowTrendingUpIcon,
  },
];

const LandingPage = () => {
  return (
    <div className="bg-white">
      {/* Hero section */}
      <div className="relative isolate overflow-hidden bg-gradient-to-b from-primary-100 to-white">
        <div className="mx-auto max-w-7xl px-6 pt-10 pb-24 sm:pb-32 lg:flex lg:px-8 lg:py-40">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
            <h1 className="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Take control of your finances
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              SpendApp helps you track your spending, analyze your habits, and achieve your financial goals.
              Connect your bank accounts and start your journey to financial freedom today.
            </p>
            <div className="mt-10 flex items-center gap-x-6">
              <Link
                to="/register"
                className="btn-primary"
              >
                Get started
              </Link>
              <Link
                to="/login"
                className="text-sm font-semibold leading-6 text-gray-900"
              >
                Log in <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Feature section */}
      <div className="mx-auto max-w-7xl px-6 lg:px-8 py-24">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-primary-600">Better Finance Management</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to manage your money
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            SpendApp provides all the tools you need to understand and improve your financial health.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
            {features.map((feature) => (
              <div key={feature.name} className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <feature.icon className="h-5 w-5 flex-none text-primary-600" aria-hidden="true" />
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">{feature.description}</p>
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  );
};

export default LandingPage; 