import React, { useState } from 'react'
import client from '../api/client'

const ExportPage: React.FC = () => {
  const today = new Date()
  const [month, setMonth] = useState(today.getMonth() + 1)
  const [year, setYear] = useState(today.getFullYear())
  const [exporting, setExporting] = useState(false)

  const handleExport = async (format: 'csv' | 'pdf') => {
    setExporting(true)
    try {
      const response = await client.get(`/api/v1/export/${format}?month=${month}&year=${year}`, {
        responseType: format === 'pdf' ? 'arraybuffer' : 'text'
      })

      const blob = new Blob(
        [response.data],
        { type: format === 'pdf' ? 'application/pdf' : 'text/csv' }
      )

      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `expenses_${year}-${String(month).padStart(2, '0')}.${format}`
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert('Erreur export')
    } finally {
      setExporting(false)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Export de dépenses</h1>

      <div className="card">
        <h3>Sélectionner la période</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px' }}>
          <div>
            <label>Mois :</label>
            <select value={month} onChange={(e) => setMonth(parseInt(e.target.value))}>
              {Array.from({ length: 12 }, (_, i) => (
                <option key={i + 1} value={i + 1}>
                  {new Date(2000, i).toLocaleString('fr-FR', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Année :</label>
            <select value={year} onChange={(e) => setYear(parseInt(e.target.value))}>
              <option value={year - 1}>{year - 1}</option>
              <option value={year}>{year}</option>
              <option value={year + 1}>{year + 1}</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <button className="primary" onClick={() => handleExport('csv')} disabled={exporting}>
            📊 Télécharger CSV
          </button>
          <button className="primary" onClick={() => handleExport('pdf')} disabled={exporting}>
            📄 Télécharger PDF
          </button>
        </div>
      </div>

      <div className="card" style={{ marginTop: '20px' }}>
        <h4>À propos des exports :</h4>
        <ul style={{ fontSize: '12px', color: '#6B6860' }}>
          <li>CSV : Format tableur (Excel, Google Sheets)</li>
          <li>PDF : Rapport mis en page</li>
          <li>Inclus : titre, montant, date, catégorie, note</li>
          <li>Total automatiquement calculé</li>
        </ul>
      </div>
    </div>
  )
}

export default ExportPage
