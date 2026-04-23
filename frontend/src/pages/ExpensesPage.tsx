import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import client from '../api/client'
import { Expense, Category } from '../types'

const ExpensesPage: React.FC = () => {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ title: '', amount: '', category_id: '', date: new Date().toISOString().split('T')[0] })

  const { data: expenses = [] } = useQuery('expenses', () => client.get('/api/v1/expenses').then(r => r.data))
  const { data: categories = [] } = useQuery('categories', () => client.get('/api/v1/categories').then(r => r.data))

  const createMutation = useMutation(
    (newExp: any) => client.post('/api/v1/expenses', newExp),
    { onSuccess: () => { queryClient.invalidateQueries('expenses'); setShowForm(false); setFormData({ title: '', amount: '', category_id: '', date: new Date().toISOString().split('T')[0] }); } }
  )

  const deleteMutation = useMutation(
    (id: string) => client.delete(`/api/v1/expenses/${id}`),
    { onSuccess: () => queryClient.invalidateQueries('expenses') }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate({
      title: formData.title,
      amount: parseFloat(formData.amount),
      category_id: formData.category_id,
      date: formData.date
    })
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>Dépenses</h1>

      <button className="primary" onClick={() => setShowForm(!showForm)} style={{ marginBottom: '20px' }}>
        {showForm ? '✕ Annuler' : '+ Nouvelle dépense'}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ marginBottom: '20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <input type="text" placeholder="Titre" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} required />
            <input type="number" step="0.01" placeholder="Montant" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} required />
            <input type="date" value={formData.date} onChange={(e) => setFormData({ ...formData, date: e.target.value })} />
            <select value={formData.category_id} onChange={(e) => setFormData({ ...formData, category_id: e.target.value })} required>
              <option value="">-- Sélectionner catégorie --</option>
              {categories.map((cat: Category) => <option key={cat.category_id} value={cat.category_id}>{cat.emoji} {cat.name}</option>)}
            </select>
          </div>
          <button className="primary" style={{ marginTop: '12px', width: '100%' }} type="submit">
            Enregistrer
          </button>
        </form>
      )}

      <div className="card">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #E0E0E0' }}>
              <th>Titre</th>
              <th>Montant</th>
              <th>Date</th>
              <th>Catégorie</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((exp: Expense) => (
              <tr key={exp.expense_id} style={{ borderBottom: '1px solid #F0EEE9' }}>
                <td>{exp.title}</td>
                <td>{parseFloat(exp.amount as any).toFixed(2)} DH</td>
                <td>{new Date(exp.date).toLocaleDateString('fr-FR')}</td>
                <td>{categories.find((c: Category) => c.category_id === exp.category_id)?.emoji || ''}</td>
                <td>
                  <button className="secondary" onClick={() => deleteMutation.mutate(exp.expense_id)} style={{ padding: '4px 8px', fontSize: '11px' }}>
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default ExpensesPage
