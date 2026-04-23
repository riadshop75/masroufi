import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import client from '../api/client'
import { Budget, Category } from '../types'

const BudgetsPage: React.FC = () => {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ category_id: '', monthly_limit: '' })

  const { data: budgets = [] } = useQuery('budgets', () => client.get('/api/v1/budgets').then(r => r.data))
  const { data: categories = [] } = useQuery('categories', () => client.get('/api/v1/categories').then(r => r.data))

  const createMutation = useMutation(
    (newBudget: any) => client.post('/api/v1/budgets', newBudget),
    { onSuccess: () => { queryClient.invalidateQueries('budgets'); setShowForm(false); setFormData({ category_id: '', monthly_limit: '' }); } }
  )

  const deleteMutation = useMutation(
    (id: string) => client.delete(`/api/v1/budgets/${id}`),
    { onSuccess: () => queryClient.invalidateQueries('budgets') }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate({
      category_id: formData.category_id,
      monthly_limit: parseFloat(formData.monthly_limit)
    })
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Budgets</h1>

      <button className="primary" onClick={() => setShowForm(!showForm)} style={{ marginBottom: '20px' }}>
        {showForm ? '✕ Annuler' : '+ Nouveau budget'}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ marginBottom: '20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <select value={formData.category_id} onChange={(e) => setFormData({ ...formData, category_id: e.target.value })} required>
              <option value="">-- Sélectionner catégorie --</option>
              {categories.map((cat: Category) => <option key={cat.category_id} value={cat.category_id}>{cat.emoji} {cat.name}</option>)}
            </select>
            <input type="number" step="0.01" placeholder="Limite mensuelle (DH)" value={formData.monthly_limit} onChange={(e) => setFormData({ ...formData, monthly_limit: e.target.value })} required />
          </div>
          <button className="primary" style={{ marginTop: '12px', width: '100%' }} type="submit">
            Créer budget
          </button>
        </form>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
        {budgets.map((budget: any) => {
          const cat = categories.find((c: Category) => c.category_id === budget.category_id)
          const isAlert = budget.percentage >= budget.alert_threshold
          const isExceeded = budget.percentage >= 100

          return (
            <div key={budget.budget_id} className="card" style={{ borderTop: `3px solid ${budget.color}` }}>
              <h3 style={{ fontSize: '14px' }}>{cat?.emoji} {cat?.name}</h3>
              <div style={{ marginTop: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                  <span>{parseFloat(budget.spent).toFixed(2)} / {parseFloat(budget.monthly_limit).toFixed(2)} DH</span>
                  <strong>{budget.percentage.toFixed(0)}%</strong>
                </div>
                <div style={{ background: '#F0EEE9', height: '6px', borderRadius: '99px', overflow: 'hidden' }}>
                  <div
                    style={{
                      background: isExceeded ? '#DC2626' : isAlert ? '#D97706' : '#16A34A',
                      height: '100%',
                      width: `${Math.min(budget.percentage, 100)}%`
                    }}
                  />
                </div>
                {isAlert && <p style={{ marginTop: '8px', fontSize: '11px', color: '#B91C1C' }}>⚠️ Limite atteinte</p>}
              </div>
              <button className="secondary" onClick={() => deleteMutation.mutate(budget.budget_id)} style={{ width: '100%', marginTop: '12px', fontSize: '11px' }}>
                Supprimer
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default BudgetsPage
