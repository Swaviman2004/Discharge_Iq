import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Download, History, Plus, AlertCircle, LogOut, User } from 'lucide-react';
import PatientForm from './components/PatientForm';
import SummaryDisplay from './components/SummaryDisplay';
import RecordsList from './components/RecordsList';
import Login from './components/Login';

function App() {
  const [currentView, setCurrentView] = useState('login');
  const [currentSummary, setCurrentSummary] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Check for existing token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('discharge_iq_token');
    const storedUser = localStorage.getItem('discharge_iq_user');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
      setCurrentView('form');
    }
  }, []);

  useEffect(() => {
    if (currentView === 'history' && isAuthenticated) {
      fetchRecords();
    }
  }, [currentView, isAuthenticated]);

  const handleLogin = (loginData) => {
    setToken(loginData.access_token);
    setUser(loginData.user);
    setIsAuthenticated(true);
    localStorage.setItem('discharge_iq_token', loginData.access_token);
    localStorage.setItem('discharge_iq_user', JSON.stringify(loginData.user));
    setCurrentView('form');
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('discharge_iq_token');
    localStorage.removeItem('discharge_iq_user');
    setCurrentView('login');
  };

  const fetchRecords = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.get(`${API_BASE_URL}/records`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setRecords(response.data);
    } catch (err) {
      let errorMessage = 'Failed to fetch records. Please try again.';
      
      if (err.response) {
        if (err.response.status === 401) {
          errorMessage = 'Session expired. Please log in again.';
          handleLogout();
        } else if (err.response.status === 429) {
          errorMessage = 'Service busy. Please try again in a moment.';
        } else if (err.response.data && err.response.data.detail) {
          errorMessage = err.response.data.detail;
        }
      } else if (err.request) {
        errorMessage = 'Network error. Please check your connection and try again.';
      }
      
      setError(errorMessage);
      console.error('Error fetching records:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = async (patientData) => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.post(`${API_BASE_URL}/generate-summary`, patientData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setCurrentSummary(response.data);
      setCurrentView('summary');
    } catch (err) {
      let errorMessage = 'Failed to generate summary. Please check your input and try again.';
      
      if (err.response) {
        // Server responded with error status
        if (err.response.status === 401) {
          errorMessage = 'Session expired. Please log in again.';
          // Auto logout on expired token
          handleLogout();
        } else if (err.response.status === 429) {
          errorMessage = 'AI service is busy. Please try again in a moment.';
        } else if (err.response.data && err.response.data.detail) {
          errorMessage = err.response.data.detail;
        }
      } else if (err.request) {
        // Network error
        errorMessage = 'Network error. Please check your connection and try again.';
      }
      
      setError(errorMessage);
      console.error('Error generating summary:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async (recordId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/download-pdf/${recordId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `discharge_summary_${recordId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download PDF. Please try again.');
      console.error('Error downloading PDF:', err);
    }
  };

  const getRiskBadgeColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low':
        return 'risk-badge-low';
      case 'medium':
        return 'risk-badge-medium';
      case 'high':
        return 'risk-badge-high';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Show Login if not authenticated */}
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center">
                  <FileText className="h-8 w-8 text-primary-600 mr-3" />
                  <h1 className="text-2xl font-bold text-gray-900">Discharge IQ</h1>
                  <span className="ml-2 text-sm text-gray-500">Smart Discharge Summary Generator</span>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <User className="h-4 w-4 mr-1" />
                    {user?.full_name} ({user?.role})
                  </div>
                  <nav className="flex space-x-4">
                    <button
                      onClick={() => setCurrentView('form')}
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        currentView === 'form'
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <Plus className="h-4 w-4 inline mr-1" />
                      New Summary
                    </button>
                    <button
                      onClick={() => setCurrentView('history')}
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        currentView === 'history'
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <History className="h-4 w-4 inline mr-1" />
                      History
                    </button>
                    <button
                      onClick={handleLogout}
                      className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900"
                    >
                      <LogOut className="h-4 w-4 inline mr-1" />
                      Logout
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Error Alert */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex">
                  <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
                  <div className="text-sm text-red-800">{error}</div>
                </div>
              </div>
            )}

            {/* Loading Indicator */}
            {loading && (
              <div className="mb-6 bg-blue-50 border border-blue-200 rounded-md p-4">
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                  <div className="text-sm text-blue-800">Processing...</div>
                </div>
              </div>
            )}

            {/* View Content */}
            {currentView === 'form' && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2">
                  <PatientForm onSubmit={handleFormSubmit} loading={loading} />
                </div>
                <div className="lg:col-span-1">
                  <div className="bg-white rounded-lg shadow-md p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">About Discharge IQ</h3>
                    <div className="space-y-3 text-sm text-gray-600">
                      <p>AI-powered discharge summary generator that:</p>
                      <ul className="list-disc list-inside space-y-1">
                        <li>Creates professional discharge summaries</li>
                        <li>Generates patient-friendly explanations</li>
                        <li>Calculates clinical risk scores</li>
                        <li>Exports downloadable PDF reports</li>
                        <li>Stores all data securely in MySQL</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {currentView === 'summary' && currentSummary && (
              <SummaryDisplay
                summary={currentSummary}
                onDownloadPDF={() => handleDownloadPDF(currentSummary.id)}
                onNewSummary={() => setCurrentView('form')}
                getRiskBadgeColor={getRiskBadgeColor}
              />
            )}

            {currentView === 'history' && (
              <RecordsList
                records={records}
                loading={loading}
                onSelectRecord={(record) => {
                  setCurrentSummary(record);
                  setCurrentView('summary');
                }}
                onDownloadPDF={handleDownloadPDF}
                getRiskBadgeColor={getRiskBadgeColor}
              />
            )}
          </main>

          {/* Footer */}
          <footer className="bg-white border-t border-gray-200 mt-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
              <div className="text-center text-sm text-gray-500">
                <p>© 2024 Discharge IQ - Smart Discharge Summary Generator</p>
                <p className="mt-1">Powered by AI & MySQL</p>
              </div>
            </div>
          </footer>
        </>
      )}
    </div>
  );
}

export default App;
