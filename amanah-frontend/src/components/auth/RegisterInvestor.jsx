import React, { useState } from 'react';
import api from '../../api/axios';

const RegisterInvestor = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    password2: '',
    phone: '',
    investmentCapacity: '',
    investmentPreference: 'moderate',
    experience: 'beginner'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [step, setStep] = useState(1);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (error) setError('');
  };

  const validateStep1 = () => {
    if (!formData.firstName.trim() || !formData.lastName.trim()) {
      setError('Please enter your full name');
      return false;
    }
    if (!formData.email.trim()) {
      setError('Please enter your email address');
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }
    if (!formData.phone.trim()) {
      setError('Please enter your phone number');
      return false;
    }
    return true;
  };

  const validateStep2 = () => {
    if (!formData.investmentCapacity) {
      setError('Please specify your investment capacity');
      return false;
    }
    return true;
  };

  const validateStep3 = () => {
    if (!formData.username.trim()) {
      setError('Please choose a username');
      return false;
    }
    if (formData.username.length < 3) {
      setError('Username must be at least 3 characters');
      return false;
    }
    if (!formData.password) {
      setError('Please enter a password');
      return false;
    }
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return false;
    }
    if (formData.password !== formData.password2) {
      setError('Passwords do not match');
      return false;
    }
    return true;
  };

  const handleNext = () => {
    if (step === 1 && validateStep1()) {
      setStep(2);
    } else if (step === 2 && validateStep2()) {
      setStep(3);
    }
  };

  const handleBack = () => {
    setStep(step - 1);
    setError('');
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validateStep3()) return;

  setIsLoading(true);
  setError('');

  try {
    const response = await api.post('/api/users/signup/investor/', {
      username: formData.username,
      email: formData.email,
      first_name: formData.firstName,
      last_name: formData.lastName,
      password: formData.password,
      password2: formData.password2,
      phone: formData.phone,
      investment_capacity: Number(formData.investmentCapacity),
      investment_preference: formData.investmentPreference,
      experience: formData.experience,
      role: 'investor',
    });

    // Axios: data is in response.data, no need for response.json()
    setSuccess(true);
    setTimeout(() => {
      window.location.href = '/login';
    }, 2500);

  } catch (err) {
    // Axios throws on 4xx/5xx — error response is in err.response.data
    const data = err.response?.data;
    const errorMessage =
      data?.username?.[0] ||
      data?.email?.[0] ||
      data?.password?.[0] ||
      data?.detail ||
      'Registration failed. Please try again.';
    setError(errorMessage);
    console.error('Registration error:', err);
  } finally {
    setIsLoading(false);
  }
};

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex w-full items-center justify-center p-4 w-screen">
        <div className="text-center animate-fadeIn max-w-md">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-6 w-screen">
            <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-3">Welcome, Investor!</h2>
          <p className="text-gray-600 mb-4">Your account has been created successfully.</p>
          <p className="text-sm text-gray-500">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4 relative overflow-hidden w-screen">
      {/* Decorative Background - Investment Theme */}
      <div className="absolute inset-0 opacity-5">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="investor-pattern" x="0" y="0" width="80" height="80" patternUnits="userSpaceOnUse">
              <circle cx="40" cy="40" r="30" fill="none" stroke="currentColor" strokeWidth="0.5" className="text-blue-600"/>
              <path d="M10 40 L70 40 M40 10 L40 70" stroke="currentColor" strokeWidth="0.5" className="text-indigo-600"/>
              <circle cx="40" cy="40" r="15" fill="none" stroke="currentColor" strokeWidth="0.5" className="text-blue-500"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#investor-pattern)"/>
        </svg>
      </div>
        <div className="w-full max-w-6xl mx-auto relative z-10">
      {/* <div className="w-full max-w-2xl relative z-10"> */}
        {/* Header */}
        <div className="text-center mb-8 animate-slideDown">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl mb-4 shadow-lg">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Investor Registration</h1>
          <p className="text-gray-600">Join Amanah as an investor and grow your wealth</p>
          <a href="/register/entrepreneur" className="text-sm text-blue-600 hover:text-blue-700 mt-2 inline-block">
            Are you an entrepreneur? Register here →
          </a>
        </div>

        {/* Progress Indicator */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full transition-all duration-300 ${
              step >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-400'
            }`}>
              <span className="text-sm font-semibold">1</span>
            </div>
            <div className={`w-12 h-1 transition-all duration-300 ${
              step >= 2 ? 'bg-blue-600' : 'bg-gray-200'
            }`}></div>
            <div className={`flex items-center justify-center w-10 h-10 rounded-full transition-all duration-300 ${
              step >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-400'
            }`}>
              <span className="text-sm font-semibold">2</span>
            </div>
            <div className={`w-12 h-1 transition-all duration-300 ${
              step >= 3 ? 'bg-blue-600' : 'bg-gray-200'
            }`}></div>
            <div className={`flex items-center justify-center w-10 h-10 rounded-full transition-all duration-300 ${
              step >= 3 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-400'
            }`}>
              <span className="text-sm font-semibold">3</span>
            </div>
          </div>
        </div>

        {/* Registration Card */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-gray-100 animate-fadeIn">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            {step === 1 && 'Personal Information'}
            {step === 2 && 'Investment Profile'}
            {step === 3 && 'Account Security'}
          </h2>
          
          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start animate-shake">
              <svg className="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span className="text-sm text-red-800">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Step 1: Personal Information */}
            {step === 1 && (
              <div className="space-y-5 animate-slideRight">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-2">
                      First Name
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                      placeholder="Ahmed"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-2">
                      Last Name
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                      placeholder="Ibrahim"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="ahmed.investor@example.com"
                  />
                </div>

                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="+234 801 234 5678"
                  />
                </div>

                <button
                  type="button"
                  onClick={handleNext}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all"
                >
                  Continue
                </button>
              </div>
            )}

            {/* Step 2: Investment Profile */}
            {step === 2 && (
              <div className="space-y-5 animate-slideLeft">
                <div>
                  <label htmlFor="investmentCapacity" className="block text-sm font-medium text-gray-700 mb-2">
                    Investment Capacity (₦)
                  </label>
                  <input
                    type="number"
                    id="investmentCapacity"
                    name="investmentCapacity"
                    value={formData.investmentCapacity}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="1000000"
                    min="0"
                  />
                  <p className="text-xs text-gray-500 mt-1">Minimum investment: ₦100,000</p>
                </div>

                <div>
                  <label htmlFor="investmentPreference" className="block text-sm font-medium text-gray-700 mb-2">
                    Risk Preference
                  </label>
                  <select
                    id="investmentPreference"
                    name="investmentPreference"
                    value={formData.investmentPreference}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                  >
                    <option value="conservative">Conservative - Lower risk, stable returns</option>
                    <option value="moderate">Moderate - Balanced risk and returns</option>
                    <option value="aggressive">Aggressive - Higher risk, higher returns</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="experience" className="block text-sm font-medium text-gray-700 mb-2">
                    Investment Experience
                  </label>
                  <select
                    id="experience"
                    name="experience"
                    value={formData.experience}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                  >
                    <option value="beginner">Beginner - New to investing</option>
                    <option value="intermediate">Intermediate - 1-3 years experience</option>
                    <option value="advanced">Advanced - 3+ years experience</option>
                  </select>
                </div>

                <div className="flex space-x-3">
                  <button
                    type="button"
                    onClick={handleBack}
                    className="flex-1 bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-all"
                  >
                    Back
                  </button>
                  <button
                    type="button"
                    onClick={handleNext}
                    className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-all"
                  >
                    Continue
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Account Security */}
            {step === 3 && (
              <div className="space-y-5 animate-slideRight">
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                    Username
                  </label>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="ahmed_investor"
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                    Password
                  </label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="At least 8 characters"
                  />
                </div>

                <div>
                  <label htmlFor="password2" className="block text-sm font-medium text-gray-700 mb-2">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="password2"
                    name="password2"
                    value={formData.password2}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="Re-enter your password"
                  />
                </div>

                <div className="flex space-x-3">
                  <button
                    type="button"
                    onClick={handleBack}
                    disabled={isLoading}
                    className="flex-1 bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-all disabled:opacity-50"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-all disabled:bg-blue-400 flex items-center justify-center"
                  >
                    {isLoading ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Creating...
                      </>
                    ) : (
                      'Create Investor Account'
                    )}
                  </button>
                </div>
              </div>
            )}
          </form>

          {step === 3 && (
            <p className="mt-4 text-xs text-center text-gray-500">
              By creating an account, you agree to our{' '}
              <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">Terms</a>
              {' '}and{' '}
              <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">Privacy Policy</a>
            </p>
          )}
        </div>

        {/* Login Link */}
        <p className="text-center mt-6 text-gray-600">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 hover:text-blue-700 font-medium">Sign in</a>
        </p>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideRight {
          from { opacity: 0; transform: translateX(-20px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideLeft {
          from { opacity: 0; transform: translateX(20px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
          20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        .animate-fadeIn { animation: fadeIn 0.5s ease-out; }
        .animate-slideDown { animation: slideDown 0.5s ease-out; }
        .animate-slideRight { animation: slideRight 0.3s ease-out; }
        .animate-slideLeft { animation: slideLeft 0.3s ease-out; }
        .animate-shake { animation: shake 0.5s ease-out; }
      `}</style>
    </div>
  );
};

export default RegisterInvestor;