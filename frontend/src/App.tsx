import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import DashboardPage from './pages/DashboardPage'
import ExpensesPage from './pages/ExpensesPage'
import CategoriesPage from './pages/CategoriesPage'
import BudgetsPage from './pages/BudgetsPage'
import ExportPage from './pages/ExportPage'

const Navigation: React.FC = () => {
  const user = JSON.parse(localStorage.getItem('user') || 'null')
  const isAuth = !!localStorage.getItem('access_token')

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }

  if (!isAuth) return null

  return (
    <nav style={{ background: '#FFFFFF', borderBottom: '1px solid #E0E0E0', padding: '12px 20px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: '20px' }}>
          <Link to="/dashboard" style={{ textDecoration: 'none', color: '#1A1917', fontWeight: 500 }}>📊 Tableau de bord</Link>
          <Link to="/expenses" style={{ textDecoration: 'none', color: '#1A1917' }}>💳 Dépenses</Link>
          <Link to="/categories" style={{ textDecoration: 'none', color: '#1A1917' }}>🏷️ Catégories</Link>
          <Link to="/budgets" style={{ textDecoration: 'none', color: '#1A1917' }}>💰 Budgets</Link>
          <Link to="/export" style={{ textDecoration: 'none', color: '#1A1917' }}>📥 Export</Link>
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{ fontSize: '12px', color: '#6B6860' }}>{user?.name}</span>
          <button className="secondary" onClick={handleLogout} style={{ padding: '6px 12px', fontSize: '11px' }}>
            Déconnexion
          </button>
        </div>
      </div>
    </nav>
  )
}

const App: React.FC = () => {
  const isAuth = !!localStorage.getItem('access_token')

  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/dashboard" element={isAuth ? <DashboardPage /> : <Navigate to="/login" />} />
        <Route path="/expenses" element={isAuth ? <ExpensesPage /> : <Navigate to="/login" />} />
        <Route path="/categories" element={isAuth ? <CategoriesPage /> : <Navigate to="/login" />} />
        <Route path="/budgets" element={isAuth ? <BudgetsPage /> : <Navigate to="/login" />} />
        <Route path="/export" element={isAuth ? <ExportPage /> : <Navigate to="/login" />} />
        <Route path="/" element={<Navigate to={isAuth ? '/dashboard' : '/login'} />} />
      </Routes>
    </Router>
  )
}

export default App
