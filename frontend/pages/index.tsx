import { useEffect, useState } from "react";

type CampaignStatus = "Active" | "Paused";

type Campaign = {
  id: number;
  name: string;
  status: CampaignStatus;
  clicks: number;
  cost: number;
  impressions: number;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function HomePage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [filterStatus, setFilterStatus] = useState<CampaignStatus | "All">(
    "All"
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCampaigns = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_BASE_URL}/campaigns`);
        if (!response.ok) {
          throw new Error("Failed to load campaigns");
        }
        const data: Campaign[] = await response.json();
        setCampaigns(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const visibleCampaigns =
    filterStatus === "All"
      ? campaigns
      : campaigns.filter((c) => c.status === filterStatus);

  return (
    <div className="page">
      <main className="container">
        <h1 className="title">Campaign Analytics Dashboard</h1>

        <section className="controls">
          <label className="filter-label">
            <span>Status filter:</span>
            <select
              value={filterStatus}
              onChange={(e) =>
                setFilterStatus(e.target.value as CampaignStatus | "All")
              }
            >
              <option value="All">All</option>
              <option value="Active">Active</option>
              <option value="Paused">Paused</option>
            </select>
          </label>
        </section>

        {isLoading && <p>Loading campaigns...</p>}
        {error && <p className="error">Error: {error}</p>}

        {!isLoading && !error && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Campaign Name</th>
                  <th>Status</th>
                  <th>Clicks</th>
                  <th>Cost ($)</th>
                  <th>Impressions</th>
                </tr>
              </thead>
              <tbody>
                {visibleCampaigns.map((campaign) => (
                  <tr key={campaign.id}>
                    <td>{campaign.name}</td>
                    <td>
                      <span
                        className={
                          campaign.status === "Active"
                            ? "badge badge-active"
                            : "badge badge-paused"
                        }
                      >
                        {campaign.status}
                      </span>
                    </td>
                    <td>{campaign.clicks}</td>
                    <td>{campaign.cost.toFixed(2)}</td>
                    <td>{campaign.impressions}</td>
                  </tr>
                ))}
                {visibleCampaigns.length === 0 && (
                  <tr>
                    <td colSpan={5} className="empty">
                      No campaigns found for this filter.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}



