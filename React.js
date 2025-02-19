import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [trades, setTrades] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [config, setConfig] = useState({});

  useEffect(() => {
    fetch("/api/trades").then(res => res.json()).then(data => setTrades(data));
    fetch("/api/alerts").then(res => res.json()).then(data => setAlerts(data));
    fetch("/api/config").then(res => res.json()).then(data => setConfig(data));
  }, []);

  const updateConfig = () => {
    fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config),
    }).then(res => res.json()).then(data => alert("Settings updated!"));
  };

  return (
    <div className="App">
      <h1>DexScreener Trading Bot</h1>

      <div className="section">
        <h2>Trade Settings</h2>
        <label>Min Liquidity</label>
        <input type="number" value={config.filters?.min_liquidity} onChange={(e) => setConfig({...config, filters: {...config.filters, min_liquidity: e.target.value}})} />
        <label>Min Volume</label>
        <input type="number" value={config.filters?.min_volume} onChange={(e) => setConfig({...config, filters: {...config.filters, min_volume: e.target.value}})} />
        <button onClick={updateConfig}>Save Settings</button>
      </div>

      <div className="section">
        <h2>Recent Trades</h2>
        <ul>
          {trades.map((trade, index) => (
            <li key={index}>{trade.name} - ${trade.price}</li>
          ))}
        </ul>
      </div>

      <div className="section">
        <h2>Alerts</h2>
        <ul>
          {alerts.map((alert, index) => (
            <li key={index}>{alert.message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
