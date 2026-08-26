import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ScanProductPage from './pages/ScanProductPage';
import InspectionDetailsPage from './pages/InspectionDetailsPage';
import OnlineListingPage from './pages/OnlineListingPage';
import InspectionHistoryPage from './pages/InspectionHistoryPage';
import ProductRepositoryPage from './pages/ProductRepositoryPage';
import RuleRepositoryPage from './pages/RuleRepositoryPage';
import { getAuthToken } from './services/api';

// Protected Route Wrapper
function ProtectedLayout() {
  const token = getAuthToken();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-900 antialiased">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/scan" element={<ScanProductPage />} />
            <Route path="/ecommerce" element={<OnlineListingPage />} />
            <Route path="/inspections" element={<InspectionHistoryPage />} />
            <Route path="/inspections/:id" element={<InspectionDetailsPage />} />
            <Route path="/products" element={<ProductRepositoryPage />} />
            <Route path="/rules" element={<RuleRepositoryPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={<ProtectedLayout />} />
      </Routes>
    </BrowserRouter>
  );
}
