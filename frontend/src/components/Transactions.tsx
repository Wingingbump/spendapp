import React from 'react';

const Transactions: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Transactions</h1>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="p-6">
          <p className="text-gray-600 dark:text-gray-400">Transaction list will be displayed here.</p>
        </div>
      </div>
    </div>
  );
};

export default Transactions; 