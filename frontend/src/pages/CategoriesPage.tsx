import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import client from '../api/client'
import { Category } from '../types'

const CategoriesPage: React.FC = () => {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', emoji: '', color: '#1D4ED8' })

  const { data: categories = [] } = useQuery('categories', () => client.get('/api/v1/categories').then(r => r.data))

  const createMutation = useMutation(
    (newCat: any) => client.post('/api/v1/categories', newCat),
    { onSuccess: () => { queryClient.invalidateQueries('categories'); setShowForm(false); setFormData({ name: '', emoji: '', color: '#1D4ED8' }); } }
  )

  const deleteMutation = useMutation(
    (id: string) => client.delete(`/api/v1/categories/${id}`),
    { onSuccess: () => queryClient.invalidateQueries('categories') }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(formData)
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>Catégories</h1>

      <button className="primary" onClick={() => setShowForm(!showForm)} style={{ marginBottom: '20px' }}>
        {showForm ? '✕ Annuler' : '+ Nouvelle catégorie'}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ marginBottom: '20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
            <input type="text" placeholder="Nom" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
            <input type="text" placeholder="Emoji" value={formData.emoji} onChange={(e) => setFormData({ ...formData, emoji: e.target.value })} maxLength={2} />
            <input type="color" value={formData.color} onChange={(e) => setFormData({ ...formData, color: e.target.value })} />
          </div>
          <button className="primary" style={{ marginTop: '12px', width: '100%' }} type="submit">
            Ajouter
          </button>
        </form>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '12px' }}>
        {categories.map((cat: Category) => (
          <div key={cat.category_id} className="card" style={{ borderLeft: `4px solid ${cat.color}` }}>
            <h3 style={{ fontSize: '16px' }}>{cat.emoji} {cat.name}</h3>
            <button className="secondary" onClick={() => deleteMutation.mutate(cat.category_id)} style={{ width: '100%', marginTop: '12px' }}>
              Supprimer
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CategoriesPage
