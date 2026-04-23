import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'

const SignupPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await client.post('/api/v1/auth/signup', { email, password, name })
      const { access_token, refresh_token, user } = response.data

      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify(user))

      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur inscription')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto', textAlign: 'center' }}>
      <h1>S'inscrire</h1>
      {error && <p style={{ color: '#DC2626' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '16px' }}>
          <input
            type="text"
            placeholder="Nom complet"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{ width: '100%' }}
          />
        </div>
        <div style={{ marginBottom: '16px' }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%' }}
          />
        </div>
        <div style={{ marginBottom: '16px' }}>
          <input
            type="password"
            placeholder="Mot de passe (min 8 caractères)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            style={{ width: '100%' }}
          />
        </div>
        <button className="primary" disabled={loading} style={{ width: '100%' }}>
          {loading ? 'Inscription...' : "S'inscrire"}
        </button>
      </form>
      <p style={{ marginTop: '20px' }}>
        Déjà un compte ? <a href="/login">Se connecter</a>
      </p>
    </div>
  )
}

export default SignupPage
