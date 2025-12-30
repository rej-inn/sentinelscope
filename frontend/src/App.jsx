import { useState } from "react";
import Submit from "./pages/Submit";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  const [history, setHistory] = useState([]);
  const [currentCase, setCurrentCase] = useState(null);
  const [stats, setStats] = useState({
    malicious: 0,
    suspicious: 0,
    low: 0,
    informational: 0,
  });

  return (
    <div className="app">
      {/* ================= HEADER ================= */}
      <header className="header">
        <h1>SentinelScope</h1>
        <span className="subtitle">Threat Intelligence & Enrichment</span>
      </header>

      {/* ================= KPI BAR ================= */}
      <div className="kpi-bar">
        <div className="kpi critical">
          <strong>{stats.malicious}</strong>
          <span>Malicious</span>
        </div>

        <div className="kpi warning">
          <strong>{stats.suspicious}</strong>
          <span>Suspicious</span>
        </div>

        <div className="kpi low">
          <strong>{stats.low}</strong>
          <span>Low</span>
        </div>

        <div className="kpi info">
          <strong>{stats.informational}</strong>
          <span>Informational</span>
        </div>
      </div>

      {/* ================= MAIN WORKSPACE ================= */}
      <div className="workspace">
        {/* -------- LEFT PANEL -------- */}
        <div className="left-panel">
          <Submit
            onResult={(result) => {
              setCurrentCase(result);
              setHistory((prev) => [result, ...prev]);

              setStats((prev) => ({
                ...prev,
                [result.severity]: prev[result.severity] + 1,
              }));
            }}
          />
        </div>

        {/* -------- RIGHT PANEL -------- */}
        <div className="right-panel">
          <h3>Active Investigation</h3>

          {currentCase ? (
            <table className="soc-table">
              <tbody>
                <tr>
                  <th>Observable</th>
                  <td>{currentCase.observable}</td>
                </tr>
                <tr>
                  <th>Type</th>
                  <td>{currentCase.type.toUpperCase()}</td>
                </tr>
                <tr>
                  <th>Severity</th>
                  <td className={`sev ${currentCase.severity}`}>
                    {currentCase.severity.toUpperCase()}
                  </td>
                </tr>
                <tr>
                  <th>Confidence</th>
                  <td>{currentCase.confidence}%</td>
                </tr>
                <tr>
                  <th>Time</th>
                  <td>{new Date().toLocaleTimeString()}</td>
                </tr>
              </tbody>
            </table>
          ) : (
            <p className="placeholder">
              Submit an observable to begin analysis.
            </p>
          )}
        </div>
      </div>

      {/* ================= HISTORY ================= */}
      <Dashboard history={history} />
    </div>
  );
}

export default App;
