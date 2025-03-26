import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { IconBaseProps } from 'react-icons';
import { FiCreditCard, FiDollarSign, FiTrendingUp } from 'react-icons/fi';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  category: string;
  merchant: string;
}

interface Summary {
  income: number;
  expenses: number;
  net: number;
  period: {
    start: string;
    end: string;
  };
  mainAccountBalance: number;
  investmentBalance: number;
  mainAccountChange: number;
  investmentChange: number;
  monthlyBalances: {
    month: string;
    balance: number;
  }[];
}

const Dashboard: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [userName, setUserName] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/me', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setUserName(data.full_name);
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [transactionsResponse, summaryResponse] = await Promise.all([
          fetch(`http://localhost:8000/api/transactions?time_period=${selectedPeriod}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }),
          fetch(`http://localhost:8000/api/summary?time_period=${selectedPeriod}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
        ]);

        if (transactionsResponse.ok && summaryResponse.ok) {
          const [transactionsData, summaryData] = await Promise.all([
            transactionsResponse.json(),
            summaryResponse.json()
          ]);

          setTransactions(transactionsData);
          setSummary(summaryData);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [selectedPeriod]);

  const chartData = {
    labels: summary?.monthlyBalances?.map(b => b.month) || [],
    datasets: [
      {
        label: 'Balance',
        data: summary?.monthlyBalances?.map(b => b.balance) || [],
        borderColor: 'rgb(16, 185, 129)',
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
      x: {
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <div className="flex-1">
      <main className="p-8 pl-12">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">Welcome back, {userName}</h1>
          <p className="text-gray-600">Here's an overview of all of your balances.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="col-span-2 bg-white p-6 rounded-xl shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium">Account Balance</h2>
              <div className="flex space-x-2">
                {['Day', 'Week', 'Month', 'Year'].map((period) => (
                  <button
                    key={period}
                    onClick={() => setSelectedPeriod(period.toLowerCase())}
                    className={`px-3 py-1 rounded-full text-sm ${
                      selectedPeriod === period.toLowerCase()
                        ? 'bg-emerald-600 text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {period}
                  </button>
                ))}
              </div>
            </div>
            <Line data={chartData} options={chartOptions} />
          </div>

          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-600">Total Balance</h3>
                <span className={`text-sm ${(summary?.net || 0) >= 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                  {(summary?.net || 0) >= 0 ? '+' : '-'}{Math.abs(summary?.mainAccountChange || 0)}%
                </span>
              </div>
              <div className="flex items-center">
                <FiDollarSign size={24} className="text-emerald-600 mr-2" />
                <span className="text-2xl font-semibold">${summary?.net.toLocaleString() || '0.00'}</span>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-600">Main Account</h3>
                <button className="text-gray-400 hover:text-gray-600">•••</button>
              </div>
              <div className="flex items-center">
                <FiCreditCard size={24} className="text-emerald-600 mr-2" />
                <span className="text-2xl font-semibold">
                  ${summary?.mainAccountBalance?.toLocaleString() || '0.00'}
                </span>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-600">Investments</h3>
                <span className={`text-sm ${(summary?.investmentChange || 0) >= 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                  {(summary?.investmentChange || 0) >= 0 ? '+' : '-'}{Math.abs(summary?.investmentChange || 0)}%
                </span>
              </div>
              <div className="flex items-center">
                <FiTrendingUp size={24} className="text-emerald-600 mr-2" />
                <span className="text-2xl font-semibold">
                  ${summary?.investmentBalance?.toLocaleString() || '0.00'}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium">Recent Transactions</h2>
              <button className="text-emerald-600 hover:text-emerald-700 text-sm font-medium">
                See all
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-gray-500 text-sm">
                  <th className="px-6 py-3">Name</th>
                  <th className="px-6 py-3">Date</th>
                  <th className="px-6 py-3">Time</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3 text-right">Amount</th>
                </tr>
              </thead>
              <tbody>
                {transactions.slice(0, 5).map((transaction) => (
                  <tr key={transaction.id} className="border-t border-gray-100">
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-emerald-100 rounded-full mr-3"></div>
                        <span>{transaction.merchant}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {new Date(transaction.date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      {new Date(transaction.date).toLocaleTimeString()}
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 bg-emerald-100 text-emerald-700 rounded-full text-sm">
                        Completed
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className={transaction.amount > 0 ? 'text-emerald-600' : 'text-red-600'}>
                        {transaction.amount > 0 ? '+' : '-'}${Math.abs(transaction.amount).toFixed(2)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard; 