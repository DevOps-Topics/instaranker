import { useEffect, useState } from "react";

export default function App() {
  const [items, setItems] = useState([]);
  const [limit, setLimit] = useState(50);
  const [api, setApi] = useState("");

  // Load config.json once on mount
  useEffect(() => {
    fetch("/config.json")
      .then(r => r.json())
      .then(cfg => setApi(cfg.API_BASE))
      .catch(err => console.error("Failed to load config.json", err));
  }, []);

  // Fetch leaderboard when API + limit are ready
  useEffect(() => {
    if (!api) return; // wait until config.json loads
    fetch(`${api}/leaderboard?limit=${limit}`)
      .then(r => r.json())
      .then(d => setItems(d.items || []))
      .catch(console.error);
  }, [api, limit]);

  return (
    <div className="max-w-4xl mx-auto p-6 font-[Inter]">
      <h1 className="text-3xl font-bold text-indigo-600">Influencer Leaderboard</h1>
      <p className="text-gray-600 mb-4">
        Ranking updates hourly from recent reels (synthetic demo data).
      </p>

      <div className="mb-4">
        <label className="mr-2 font-medium">Show:</label>
        <select
          className="border rounded px-2 py-1"
          value={limit}
          onChange={e => setLimit(Number(e.target.value))}
        >
          {[10, 25, 50, 100].map(n => (
            <option key={n} value={n}>{n}</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto shadow rounded-lg">
        <table className="w-full border-collapse">
          <thead className="bg-indigo-50 text-indigo-700">
            <tr>
              <th className="p-2 text-left">Rank</th>
              <th className="p-2 text-left">Handle</th>
              <th className="p-2 text-right">Score</th>
              <th className="p-2 text-right">Followers</th>
              <th className="p-2 text-right">Avg Views</th>
              <th className="p-2 text-right">Consistency</th>
            </tr>
          </thead>
          <tbody>
            {items.map(it => (
              <tr
                key={it.SK}
                className="border-t hover:bg-indigo-50 transition-colors"
              >
                <td className="p-2">{it.rank}</td>
                <td className="p-2">@{it.handle}</td>
                <td className="p-2 text-right">{it.score.toFixed(1)}</td>
                <td className="p-2 text-right">{it.followers.toLocaleString()}</td>
                <td className="p-2 text-right">
                  {Math.round(it.recent_avg_views).toLocaleString()}
                </td>
                <td className="p-2 text-right">
                  {(it.consistency * 100).toFixed(0)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <footer className="mt-6 text-gray-500 text-sm">
        Demo project. No platform data used; all stats are synthetic.
      </footer>
    </div>
  );
}
