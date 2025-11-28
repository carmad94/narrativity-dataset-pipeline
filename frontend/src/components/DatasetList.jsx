import React, { useEffect, useState, useCallback } from "react";
import { listBronze } from "../api";

export default function DatasetList({onSelect, selectedId}) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pageSize, setPageSize] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const load = useCallback(async () => {
  setLoading(true);
  setError(null);
  try {
    const offset = currentPage;
    const data = await listBronze(offset, pageSize);
    setRecords(Array.isArray(data.records) ? data.records : []);
    setTotalCount(data.total);
    console.log(data.total)
    console.log(pageSize)
  } catch (err) {
    console.error(err);
    setError(err?.response?.data?.message || err.message || "Failed to load datasets");
  } finally {
    setLoading(false);
  }
}, [currentPage, pageSize]);

useEffect(() => {
  load();
}, [load]);

  const totalPages = Math.ceil(totalCount / pageSize);

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const handlePageSizeChange = (e) => {
    setPageSize(Number(e.target.value));
    setCurrentPage(1); // reset to first page
  };

  if (loading) return <p>Loading uploaded datasets...</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-3">Uploaded datasets (Bronze)</h3>

      <div className="mb-4 flex items-center gap-4">
        <label htmlFor="pageSize" className="text-sm">Records per page:</label>
        <select
          id="pageSize"
          value={pageSize}
          onChange={handlePageSizeChange}
          className="border rounded px-2 py-1"
        >
          {[10, 25, 50, 100].map((size) => (
            <option key={size} value={size}>{size}</option>
          ))}
        </select>
      </div>

      {records.length === 0 ? (
        <p>No uploaded datasets found.</p>
      ) : (
        <>
          <table className="min-w-full border border-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Paper</th>
                <th className="px-4 py-2 text-left">Connectivity</th>
                <th className="px-4 py-2 text-left">Conjunctions</th>
                <th className="px-4 py-2 text-left">Sensory Language</th>
                <th className="px-4 py-2 text-left">Setting</th>
                <th className="px-4 py-2 text-left">Narrative Perspective</th>
                <th className="px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id || r.hash || JSON.stringify(r)}
                 className={`border-t ${selectedId === (r.id || r.hash) ? "bg-blue-100" : ""}`}>
                  <td className="px-4 py-2">
                      <b>{r.title || "—"}</b>
                      <p className="text-sm">{r.author || "—"}  &middot;
                      <i className="text-sm">{r.publication_year || "—"}</i>
                      </p>
                      <button className="px-2 py-2 rounded outline-black text-white text-xs bg-sky-500/100">{r.source || "—"}</button>
                   </td>
                  <td className="px-4 py-2">{r.connectivity || "—"}</td>
                  <td className="px-4 py-2">{r.conjunctions || "—"}</td>
                  <td className="px-4 py-2">{r.sensory_language || "—"}</td>
                  <td className="px-4 py-2">{r.setting || "—"}</td>
                  <td className="px-4 py-2">{r.narrative_perspective || "—"}</td>
                  <td className="px-4 py-2">
                    <button
                        onClick={() => onSelect(r.id || r.hash)}
                        className="text-blue-600 hover:underline"
                    >
                        Explain Scores
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="flex justify-between items-center mt-4">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="px-3 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
            >
              Previous
            </button>
            <span className="text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="px-3 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      )}

      <div className="mt-4">
        <button onClick={load} className="px-3 py-2 bg-gray-200 rounded hover:bg-gray-300">
          Refresh
        </button>
      </div>
    </div>
  );
}
