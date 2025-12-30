export default function Dashboard({ history }) {
  if (!history || history.length === 0) return null;

  return (
    <div className="history">
      <h3>Analysis History</h3>

      <table className="history-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Observable</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {history.map((r, i) => (
            <tr key={i}>
              <td>{new Date().toLocaleTimeString()}</td>
              <td>{r.observable}</td>
              <td>{r.type.toUpperCase()}</td>
              <td className={`sev ${r.severity.toLowerCase()}`}>
                {r.severity.toUpperCase()}
              </td>
              <td>{r.confidence}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
