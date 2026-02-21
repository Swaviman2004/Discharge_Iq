import React from 'react';
import { Download, ArrowLeft, FileText, User, AlertTriangle, CheckCircle, Clock, Pill, Calendar } from 'lucide-react';
import { format } from 'date-fns';

const SummaryDisplay = ({ summary, onDownloadPDF, onNewSummary, getRiskBadgeColor }) => {
  const getRiskIcon = (level) => {
    switch (level?.toLowerCase()) {
      case 'low':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'medium':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
      case 'high':
        return <AlertTriangle className="h-5 w-5 text-red-600" />;
      default:
        return <Clock className="h-5 w-5 text-gray-600" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Discharge Summary</h2>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center">
                <User className="h-4 w-4 mr-1" />
                {summary.patient_name}
              </div>
              <div className="flex items-center">
                <Calendar className="h-4 w-4 mr-1" />
                {format(new Date(summary.created_at), 'MMM dd, yyyy HH:mm')}
              </div>
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={onNewSummary}
              className="btn-secondary flex items-center"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              New Summary
            </button>
            <button
              onClick={onDownloadPDF}
              className="btn-success flex items-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Download PDF
            </button>
          </div>
        </div>

        {/* Risk Badge */}
        <div className="flex items-center space-x-2">
          {getRiskIcon(summary.risk_level)}
          <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getRiskBadgeColor(summary.risk_level)}`}>
            Risk Level: {summary.risk_level} (Score: {summary.risk_score})
          </span>
        </div>
      </div>

      {/* Patient Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <User className="h-5 w-5 mr-2 text-primary-600" />
          Patient Information
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-500">Name</p>
            <p className="text-gray-900">{summary.patient_name}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Age</p>
            <p className="text-gray-900">{summary.age} years</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Gender</p>
            <p className="text-gray-900">{summary.gender}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Admission Date</p>
            <p className="text-gray-900">{format(new Date(summary.admission_date), 'MMM dd, yyyy')}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Discharge Date</p>
            <p className="text-gray-900">{format(new Date(summary.discharge_date), 'MMM dd, yyyy')}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Length of Stay</p>
            <p className="text-gray-900">
              {Math.ceil((new Date(summary.discharge_date) - new Date(summary.admission_date)) / (1000 * 60 * 60 * 24))} days
            </p>
          </div>
        </div>
      </div>

      {/* Clinical Information */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Diagnosis</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{summary.diagnosis}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Procedures</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{summary.procedures}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Laboratory Results</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{summary.lab_results}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Pill className="h-5 w-5 mr-2 text-primary-600" />
            Discharge Medications
          </h3>
          <p className="text-gray-700 whitespace-pre-wrap">{summary.medications}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Hospital Course</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{summary.hospital_course}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Follow-up Instructions</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{summary.follow_up}</p>
        </div>
      </div>

      {/* AI-Generated Summaries */}
      {summary.ai_summary && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <FileText className="h-5 w-5 mr-2 text-primary-600" />
            AI-Generated Professional Summary
          </h3>
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
            <p className="text-gray-700 whitespace-pre-wrap">{summary.ai_summary}</p>
          </div>
        </div>
      )}

      {summary.patient_summary && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <User className="h-5 w-5 mr-2 text-green-600" />
            Patient-Friendly Summary
          </h3>
          <div className="bg-green-50 border border-green-200 rounded-md p-4">
            <p className="text-gray-700 whitespace-pre-wrap">{summary.patient_summary}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SummaryDisplay;
