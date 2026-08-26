// Frontend API Service client with JWT token management and error handling

const API_BASE = '/api';

export const getAuthToken = () => {
  return localStorage.getItem('lmo_token');
};

export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('lmo_token', token);
  } else {
    localStorage.removeItem('lmo_token');
  }
};

export const getOfficerProfile = () => {
  const profile = localStorage.getItem('lmo_officer');
  return profile ? JSON.parse(profile) : null;
};

export const setOfficerProfile = (officer) => {
  if (officer) {
    localStorage.setItem('lmo_officer', JSON.stringify(officer));
  } else {
    localStorage.removeItem('lmo_officer');
  }
};

export const logoutOfficer = () => {
  localStorage.removeItem('lmo_token');
  localStorage.removeItem('lmo_officer');
  window.location.href = '/login';
};

const customFetch = async (endpoint, options = {}) => {
  const token = getAuthToken();
  const headers = {
    ...(options.headers || {}),
  };

  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // If body is not FormData, default to application/json
  if (options.body && !(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    logoutOfficer();
    throw new Error('Session expired or unauthorized. Please log in again.');
  }

  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errorDetail;
    } catch {
      errorDetail = response.statusText;
    }
    throw new Error(errorDetail);
  }

  return response.json();
};

export const api = {
  // Auth
  login: async (officer_id, password) => {
    const res = await customFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ officer_id, password }),
    });
    setAuthToken(res.access_token);
    setOfficerProfile(res.officer);
    return res;
  },
  getMe: () => customFetch('/auth/me'),

  // Products & Scanning
  uploadProduct: (formData) => customFetch('/products/upload', {
    method: 'POST',
    body: formData,
  }),
  analyzeProduct: (formData) => customFetch('/products/analyze', {
    method: 'POST',
    body: formData,
  }),
  getProducts: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return customFetch(`/products${query ? `?${query}` : ''}`);
  },
  getProductById: (id) => customFetch(`/products/${id}`),

  // Inspections
  createInspection: (payload) => customFetch('/inspections', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
  getInspections: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return customFetch(`/inspections${query ? `?${query}` : ''}`);
  },
  getInspectionById: (id) => customFetch(`/inspections/${id}`),
  verifyInspection: (id, payload) => customFetch(`/inspections/${id}/verify`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  }),
  updateViolationStatus: (inspectionId, violationId, status) => customFetch(`/inspections/${inspectionId}/violations/${violationId}`, {
    method: 'PUT',
    body: JSON.stringify({ status }),
  }),

  // Rules
  getRules: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return customFetch(`/rules${query ? `?${query}` : ''}`);
  },
  createRule: (ruleData) => customFetch('/rules', {
    method: 'POST',
    body: JSON.stringify(ruleData),
  }),
  updateRule: (id, ruleData) => customFetch(`/rules/${id}`, {
    method: 'PUT',
    body: JSON.stringify(ruleData),
  }),
  toggleRule: (id) => customFetch(`/rules/${id}/toggle`, {
    method: 'POST',
  }),

  // E-Commerce
  verifyEcommerce: (payload) => customFetch('/ecommerce/verify', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),

  // Dashboard
  getDashboardStats: () => customFetch('/dashboard/statistics'),

  // PDF Report
  generateReport: (inspectionId) => customFetch(`/reports/${inspectionId}/generate`, {
    method: 'POST',
  }),
  getReportDownloadUrl: (inspectionId) => `/api/reports/${inspectionId}/download`,
};
