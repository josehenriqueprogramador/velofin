import React, { useState } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { FaSearch, FaChartLine, FaDollarSign } from "react-icons/fa"
import "./App.sass"

function App() {
  const [ticker, setTicker] = useState("PETR4")
  const [ano, setAno] = useState(2024)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`https://velofin-api.onrender.com/api/v1/analytics?ticker=${ticker}&ano=${ano}`)
      const json = await response.json()
      
      if (!response.ok) throw new Error(json.detail || "Erro ao buscar dados")
      setData(json)
    } catch (err) {
      setError(err.message)
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="velofin-container">
      <div className="content-wrapper">
        <header>
          <h1>VELOFIN</h1>
        </header>

        <section className="search-card">
          <form onSubmit={handleSearch}>
            <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value)} />
            <input type="number" value={ano} onChange={(e) => setAno(e.target.value)} />
            <button type="submit"><FaSearch /> Analisar</button>
          </form>
        </section>

        {loading && <p style={{textAlign: 'center'}}>Buscando...</p>}
        {error && <div className="error-message">{error}</div>}

        {data && (
          <div className="dashboard-results">
            <div className="metric-card" style={{ padding: '20px', textAlign: 'center' }}>
              <h3><FaDollarSign /> Preço Atual</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>R$ {data.currentPrice}</p>
            </div>

            <div className="chart-card">
              <h3><FaChartLine /> Histórico de {data.ticker}</h3>
              <div style={{ width: '100%', height: 350 }}>
                <ResponsiveContainer>
                  <LineChart data={data.history}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                    <XAxis dataKey="date" stroke="#ccc" />
                    <YAxis domain={['auto', 'auto']} stroke="#ccc" />
                    <Tooltip contentStyle={{backgroundColor: '#1e293b'}} />
                    <Line type="monotone" dataKey="close" stroke="#38bdf8" strokeWidth={3} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
