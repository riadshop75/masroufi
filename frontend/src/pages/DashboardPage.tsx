import React, { useState } from 'react'
import { useQuery } from 'react-query'
import client from '../api/client'
import { DashboardData } from '../types'

const DashboardPage: React.FC = () => {
  const today = new Date()
  const [month, setMonth] = useState(today.getMonth() + 1)
  const [year, setYear] = useState(today.getFullYear())

  const { data, isLoading, error } = useQuery(
    ['dashboard', month, year],
    () => client.get(`/api/v1/dashboard?month=${month}&year=${year}`).then(r => r.data),
    { enabled: !!localStorage.getItem('access_token') }
  )

  if (!localStorage.getItem('access_token')) return <p>Non authentifié</p>
  if (isLoading) return <p>Chargement...</p>
  if (error) return <p>Erreur chargement dashboard</p>

  const dashboard = data as DashboardData

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Tableau de Bord</h1>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '20px' }}>
        <div className="card">
          <p className="text-muted">Aujourd'hui</p>
          <h3>{dashboard.stats.today} {dashboard.stats.currency}</h3>
        </div>
        <div className="card">
          <p className="text-muted">Ce mois</p>
          <h3>{dashboard.stats.total} {dashboard.stats.currency}</h3>
        </div>
        <div className="card">
          <p className="text-muted">Budgets</p>
          <h3>{dashboard.budget_summary?.budgets_alert || 0} alertes</h3>
        </div>
      </div>

      {/* Sélecteur mois */}
      <div style={{ marginBottom: '20px' }}>
        <label>
          Mois :{' '}
          <select value={month} onChange={(e) => setMonth(parseInt(e.target.value))}>
            {Array.from({ length: 12 }, (_, i) => (
              <option key={i + 1} value={i + 1}>
                {new Date(2000, i).toLocaleString('fr-FR', { month: 'long' })}
              </option>
            ))}
          </select>
        </label>
        {' '}
        <label>
          Année :{' '}
          <select value={year} onChange={(e) => setYear(parseInt(e.target.value))}>
            <option value={year - 1}>{year - 1}</option>
            <option value={year}>{year}</option>
            <option value={year + 1}>{year + 1}</option>
          </select>
        </label>
      </div>

      {/* Répartition par catégorie */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3>Répartition par catégorie</h3>
        {dashboard.breakdown.map((cat) => (
          <div key={cat.category_id} style={{ marginBottom: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span>
                {cat.emoji} {cat.category_name}
              </span>
              <strong>{cat.percentage.toFixed(1)}%</strong>
            </div>
            <div style={{ background: '#F0EEE9', height: '6px', borderRadius: '99px', overflow: 'hidden' }}>
              <div style={{ background: cat.color, height: '100%', width: `${cat.percentage}%` }} />
            </div>
          </div>
        ))}
      </div>

      {/* Tendance */}
      <div className="card">
        <h3>Tendance (6 derniers mois)</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #E0E0E0' }}>
              <th>Mois</th>
              <th style={{ textAlign: 'right' }}>Montant</th>
            </tr>
          </thead>
          <tbody>
            {dashboard.trend.map((t) => (
              <tr key={`${t.year}-${t.month}`} style={{ borderBottom: '1px solid #F0EEE9' }}>
                <td>
                  {new Date(t.year, t.month - 1).toLocaleString('fr-FR', {
                    month: 'short',
                    year: '2-digit',
                  })}
                </td>
                <td style={{ textAlign: 'right' }}>{parseFloat(t.amount as any).toFixed(2)} DH</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default DashboardPage
