import React, { useState, useEffect } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { FaSearch, FaChartLine, FaDollarSign } from "react-icons/fa"
import "./App.sass"

function App() {
  const [ticker, setTicker] = useState("PETR4.SA")
  const [ano, setAno] = useState(2024)
  const [searchTicker, setSearchTicker] = useState("PETR4.SA")
  const [searchAno, setSearchAno] = useState(2024)
  
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(`http://localhost:8000/api/v1/analytics?ticker=${searchTicker}&ano=${searchAno}`)
        if (!response.ok) {
          throw new Error("Ativo não encontrado ou falha no processamento.")
        }
        const json = await response.json()
        setData(json)
      } catch (err) {
        setError(err.message)
        setData(null)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [searchTicker, searchAno])

  const handleSearch = (e) => {
    e.preventDefault()
    if (ticker.trim()) {
      setSearchTicker(ticker.toUpperCase())
      setSearchAno(ano)
    }
  }

  return (
    <div className="velofin-container">
      <div className="content-wrapper">
        
        <header>
          <h1>VELOFIN</h1>
          <p>Análise Quantitativa e Inteligência Visual de Ativos</p>
        </header>

        <section className="search-card">
          <form onSubmit={handleSearch}>
            <div className="input-group">
              <label>Ticker do Ativo</label>
              <input 
                type="text" 
                value={ticker} 
                onChange={(e) => setTicker(e.target.value)} 
                placeholder="Ex: VALE3.SA, AAPL"
              />
            </div>
            <div className="input-group">
              <label>Ano Inicial</label>
              <input 
                type="number" 
                value={ano} 
                onChange={(e) => setAno(parseInt(e.target.value) || 2024)}
                min="2000" 
                max={new Date().getFullYear()}
              />
            </div>
            <button type="submit">
              <FaSearch /> Analisar
            </button>
          </form>
        </section>

        {loading && <p style={{ textAlign: 'center', color: '#38bdf8' }}>Buscando e processando dados com Pandas...</p>}
        
        {error && <div className="error-message">{error}</div>}

        {data && !loading && (
          <>
            <div className="dashboard-grid">
              <div className="metric-card">
                <h3><FaDollarSign /> Preço Atual</h3>
                <p className="price">R$ {data.currentPrice}</p>
                <span className="ticker-badge">{data.ticker}</span>
              </div>
            </div>

            <div className="chart-card">
              <h3><FaChartLine style={{ color: '#38bdf8' }} /> Histórico de Fechamento</h3>
              <div style={{ width: '100%', height: 350 }}>
                <ResponsiveContainer>
                  <LineChart data={data.history} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="date" stroke="#94a3b8" tickSize={10} />
                    <YAxis stroke="#94a3b8" domain={['auto', 'auto']} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', color: '#f8fafc' }}
                      labelStyle={{ color: '#38bdf8' }}
                    />
                    <Line type="monotone" dataKey="close" stroke="#38bdf8" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}

      </div>
    </div>
  )
}

export default App
