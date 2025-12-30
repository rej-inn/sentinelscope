export default function KPIBar({ stats }) {
  return (
    <div className="kpi-bar">
      <div className="kpi critical">Malicious<br /><strong>{stats.malicious}</strong></div>
      <div className="kpi warning">Suspicious<br /><strong>{stats.suspicious}</strong></div>
      <div className="kpi low">Clean<br /><strong>{stats.clean}</strong></div>
      <div className="kpi info">Total<br /><strong>{stats.total}</strong></div>
    </div>
  );
}
