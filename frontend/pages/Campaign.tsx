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

export default function CampaignPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [filterStatus, setFilterStatus] = useState<CampaignStatus | "All">(
    "All"
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [togglingId, setTogglingId] = useState<number | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newCampaignName, setNewCampaignName] = useState("");
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    const fetchCampaigns = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_BASE_URL}/Campaign`);
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

  const toggleStatus = async (campaignId: number) => {
    setTogglingId(campaignId);
    setError(null);
    try {
      const response = await fetch(
        `${API_BASE_URL}/Campaign/${campaignId}/toggle-status`,
        {
          method: "PATCH",
        }
      );
      if (!response.ok) {
        throw new Error("Failed to toggle status");
      }
      const updatedCampaign: Campaign = await response.json();
      
      // Update the campaign in the local state
      setCampaigns((prev) =>
        prev.map((c) => (c.id === campaignId ? updatedCampaign : c))
      );
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setTogglingId(null);
    }
  };

  const createCampaign = async () => {
    if (!newCampaignName.trim()) {
      setError("Campaign name is required");
      return;
    }

    setIsCreating(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/Campaign`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: newCampaignName.trim(),
          status: "Active",
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to create campaign");
      }
      const newCampaign: Campaign = await response.json();
      
      // Add the new campaign to the list
      setCampaigns((prev) => [...prev, newCampaign]);
      setNewCampaignName("");
      setShowAddForm(false);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsCreating(false);
    }
  };

  const visibleCampaigns =
    filterStatus === "All"
      ? campaigns
      : campaigns.filter((c) => c.status === filterStatus);

  return (
    <div className="page">
      <main className="container">
        <h1 className="title">Campaign Analytics Dashboard</h1>

        <section className="controls">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="add-btn"
          >
            {showAddForm ? "Cancel" : "+ Add Campaign"}
          </button>
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

        {showAddForm && (
          <section className="add-form">
            <h2>Add New Campaign</h2>
            <div className="form-group">
              <input
                type="text"
                placeholder="Campaign Name"
                value={newCampaignName}
                onChange={(e) => setNewCampaignName(e.target.value)}
                className="form-input"
                onKeyPress={(e) => {
                  if (e.key === "Enter") {
                    createCampaign();
                  }
                }}
              />
              <button
                onClick={createCampaign}
                disabled={isCreating || !newCampaignName.trim()}
                className="submit-btn"
              >
                {isCreating ? "Creating..." : "Create Campaign"}
              </button>
            </div>
            <p className="form-hint">
              New campaigns start with: Status=Active, Clicks=0, Cost=$0.00, Impressions=0
            </p>
          </section>
        )}

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
                      <button
                        onClick={() => toggleStatus(campaign.id)}
                        disabled={togglingId === campaign.id}
                        className={`toggle-btn ${
                          campaign.status === "Active"
                            ? "toggle-btn-active"
                            : "toggle-btn-paused"
                        }`}
                        title={`Click to switch to ${
                          campaign.status === "Active" ? "Paused" : "Active"
                        }`}
                      >
                        {togglingId === campaign.id
                          ? "..."
                          : campaign.status}
                      </button>
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


