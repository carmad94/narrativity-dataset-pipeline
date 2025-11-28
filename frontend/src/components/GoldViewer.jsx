import React, { useEffect, useState } from "react";
import { fetchGoldById } from "../api";

export default function GoldViewer({id, onBack}) {
  const [gold, setGold] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchGoldById(id);
        setGold(data);
      } catch (err) {
        console.error(err);
        setError(err?.response?.data?.message || err.message || "Failed to fetch gold data");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  if (!id) return <p>No id provided.</p>;
  if (loading) return <p>Loading gold/enriched data for {id}...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  // Try to extract likely fields from enriched data
  const enriched = gold?.enriched_data || gold?.enrichment || gold;

  return (
    <div style={{ padding: 12 }}>
        <button onClick={onBack} className="mb-4 text-sm text-gray-600 hover:underline">
        Back to Dataset list
      </button>
      <h3>Gold / Enriched record</h3>
      <p>
        <strong>ID:</strong> {id}
      </p>

      {enriched ? (
        <>
          <h4>Explanation</h4>
          <div style={{ background: "#fffbe6", padding: 8, borderRadius: 4 }}>
            {typeof enriched === "object" && (enriched.summary || enriched.enrichment || enriched.narrative) ? (
              <>
                <p>{enriched.summary || enriched.enrichment || enriched.narrative}</p>
              </>
            ) : typeof enriched === "string" ? (
              <p>{enriched}</p>
            ) : (
              <p>No narrative summary found in enriched data.</p>
            )}
          </div>
        </>
      ) : (
        <p>No enriched record found for this ID.</p>
      )}
    </div>
  );
}