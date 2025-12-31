import { useState } from "react";
import { submitObservable } from "../services/api";

const styles = `
.result-card {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 6px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

/* SOC Severity Badge */
.severity-badge {
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.75rem;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.severity-badge.informational { background: #2563eb; color: #fff; }
.severity-badge.low { background: #16a34a; color: #fff; }
.severity-badge.suspicious { background: #f59e0b; color: #000; }
.severity-badge.malicious { background: #dc2626; color: #fff; }

.confidence {
  font-size: 0.8rem;
  opacity: 0.85;
}

.result-body p {
  margin: 0.3rem 0;
}

.result-section h4 {
  margin-top: 1.2rem;
  margin-bottom: 0.5rem;
}

/* Intel table */
.intel-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.intel-table th,
.intel-table td {
  padding: 8px;
  border-bottom: 1px solid #333;
}

.intel-table th {
  text-align: left;
  opacity: 0.7;
}

.intel-verdict.malicious { color: #f87171; }
.intel-verdict.suspicious { color: #fbbf24; }
.intel-verdict.clean { color: #4ade80; }
`;

export default function Submit({ onResult, updateStats }) {
  const [value, setValue] = useState("");
  const [type, setType] = useState("ip");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!value.trim()) return;

    try {
      setLoading(true);

      const res = await submitObservable({ type, value });

      const normalized = {
        ...res.data,
        time: new Date().toLocaleTimeString(),
      };

      setResult(normalized);
      setError(null);

      // Active Investigation
      onResult?.(normalized);

      // KPI Counters
      updateStats?.(prev => {
        const next = { ...prev, total: prev.total + 1 };

        if (normalized.severity === "malicious") next.malicious += 1;
        else if (normalized.severity === "suspicious") next.suspicious += 1;
        else next.clean += 1;

        return next;
      });

    } catch (err) {
      console.error(err);
      setError("Analysis failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <style>{styles}</style>

      <h3>Submit Observable</h3>

      <select value={type} onChange={e => setType(e.target.value)}>
        <option value="ip">IP</option>
        <option value="domain">Domain</option>
        <option value="hash">Hash</option>
      </select>

      <input
        placeholder="Observable value"
        value={value}
        onChange={e => setValue(e.target.value)}
      />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      <h3>Analysis Results</h3>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div className="result-card">
          <div className="result-header">
            <div className={`severity-badge ${result.severity.toLowerCase()}`}>
              {result.severity.toUpperCase()}
            </div>
            <div className="confidence">
              Confidence: {result.confidence}%
            </div>
          </div>

          <div className="result-body">
            <p><strong>Observable:</strong> {result.observable}</p>
            <p><strong>Type:</strong> {result.type.toUpperCase()}</p>
            <p><strong>Time:</strong> {result.time}</p>
          </div>

          {/* MITRE */}
          {Array.isArray(result.mitre_attack) && result.mitre_attack.length > 0 && (
            <div className="result-section">
              <h4>MITRE ATT&CK</h4>
              <ul>
                {result.mitre_attack.map((t, i) => (
                  <li key={i}>
                    <strong>{t.id}</strong> — {t.name}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 🔥 Threat Intelligence Sources */}
          {Array.isArray(result.enrichment) && result.enrichment.length > 0 && (
            <div className="result-section">
              <h4>Threat Intelligence Sources</h4>

              <table className="intel-table">
                <thead>
                  <tr>
                    <th>Source</th>
                    <th>Verdict</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {result.enrichment
                    .filter(e => e && e.source)
                    .map((e, i) => (
                      <tr key={i}>
                        <td>{e.source}</td>
                        <td className={`intel-verdict ${e.reputation}`}>
                          {e.reputation?.toUpperCase() || "UNKNOWN"}
                        </td>
                        <td>{e.confidence ?? "-"}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
