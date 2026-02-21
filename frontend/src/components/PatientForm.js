import React, { useState } from 'react';
import { User, Calendar, Activity, Pill, FileText, Clock } from 'lucide-react';

const PatientForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    patient_name: '',
    age: '',
    gender: '',
    admission_date: '',
    discharge_date: '',
    diagnosis: '',
    procedures: '',
    lab_results: '',
    medications: '',
    hospital_course: '',
    follow_up: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation
    const requiredFields = ['patient_name', 'age', 'gender', 'admission_date', 'discharge_date', 
                          'diagnosis', 'procedures', 'lab_results', 'medications', 
                          'hospital_course', 'follow_up'];
    
    const missingFields = requiredFields.filter(field => !formData[field]);
    if (missingFields.length > 0) {
      alert('Please fill in all required fields');
      return;
    }

    // Convert age to number and dates to Date objects
    const submissionData = {
      ...formData,
      age: parseInt(formData.age),
      admission_date: new Date(formData.admission_date).toISOString().split('T')[0],
      discharge_date: new Date(formData.discharge_date).toISOString().split('T')[0]
    };

    onSubmit(submissionData);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
        <User className="h-6 w-6 mr-2 text-primary-600" />
        Patient Information
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="form-label">Patient Name *</label>
            <input
              type="text"
              name="patient_name"
              value={formData.patient_name}
              onChange={handleChange}
              className="form-input"
              placeholder="John Doe"
              required
            />
          </div>
          
          <div>
            <label className="form-label">Age *</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleChange}
              className="form-input"
              placeholder="65"
              min="0"
              max="150"
              required
            />
          </div>
          
          <div>
            <label className="form-label">Gender *</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="form-input"
              required
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        {/* Dates */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="form-label flex items-center">
              <Calendar className="h-4 w-4 mr-1 text-gray-500" />
              Admission Date *
            </label>
            <input
              type="date"
              name="admission_date"
              value={formData.admission_date}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>
          
          <div>
            <label className="form-label flex items-center">
              <Calendar className="h-4 w-4 mr-1 text-gray-500" />
              Discharge Date *
            </label>
            <input
              type="date"
              name="discharge_date"
              value={formData.discharge_date}
              onChange={handleChange}
              className="form-input"
              min={formData.admission_date}
              required
            />
          </div>
        </div>

        {/* Medical Information */}
        <div>
          <label className="form-label flex items-center">
            <Activity className="h-4 w-4 mr-1 text-gray-500" />
            Primary Diagnosis *
          </label>
          <textarea
            name="diagnosis"
            value={formData.diagnosis}
            onChange={handleChange}
            className="form-input"
            rows="3"
            placeholder="e.g., Community-acquired pneumonia, Type 2 Diabetes Mellitus"
            required
          />
        </div>

        <div>
          <label className="form-label flex items-center">
            <FileText className="h-4 w-4 mr-1 text-gray-500" />
            Procedures Performed *
          </label>
          <textarea
            name="procedures"
            value={formData.procedures}
            onChange={handleChange}
            className="form-input"
            rows="3"
            placeholder="e.g., Chest X-ray, Blood cultures, IV antibiotics"
            required
          />
        </div>

        <div>
          <label className="form-label flex items-center">
            <Activity className="h-4 w-4 mr-1 text-gray-500" />
            Laboratory Results *
          </label>
          <textarea
            name="lab_results"
            value={formData.lab_results}
            onChange={handleChange}
            className="form-input"
            rows="3"
            placeholder="e.g., WBC: 15.2 x 10^9/L, CRP: 45 mg/L, Glucose: 180 mg/dL"
            required
          />
        </div>

        <div>
          <label className="form-label flex items-center">
            <Pill className="h-4 w-4 mr-1 text-gray-500" />
            Discharge Medications *
          </label>
          <textarea
            name="medications"
            value={formData.medications}
            onChange={handleChange}
            className="form-input"
            rows="3"
            placeholder="e.g., Amoxicillin 500mg TID x 7 days, Metformin 500mg BID"
            required
          />
        </div>

        <div>
          <label className="form-label flex items-center">
            <Clock className="h-4 w-4 mr-1 text-gray-500" />
            Hospital Course *
          </label>
          <textarea
            name="hospital_course"
            value={formData.hospital_course}
            onChange={handleChange}
            className="form-input"
            rows="4"
            placeholder="Describe the patient's progress during hospitalization"
            required
          />
        </div>

        <div>
          <label className="form-label flex items-center">
            <Calendar className="h-4 w-4 mr-1 text-gray-500" />
            Follow-up Instructions *
          </label>
          <textarea
            name="follow_up"
            value={formData.follow_up}
            onChange={handleChange}
            className="form-input"
            rows="3"
            placeholder="e.g., Follow up with PCP in 1 week, Repeat chest X-ray in 4 weeks"
            required
          />
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className={`btn-primary ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Generating Summary...
              </>
            ) : (
              'Generate Discharge Summary'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PatientForm;
