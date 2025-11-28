import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Upload a file to the backend upload endpoint.
 * Expects a multipart/form-data upload at POST /upload
 * Returns the JSON response from the server.
 */
export async function uploadFile(file) {
  const fd = new FormData();
  fd.append("file", file);

  const resp = await axios.post(`${API_URL}/upload`, fd, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 120000
  });
  return resp.data;
}

/**
 * List records from the bronze table (raw uploads).
 * Expects GET /bronze or configurable endpoint.
 */
export async function listBronze(page=1, page_size=10) {
  const resp = await axios.get(
    `${API_URL}/bronze`,{
    params: {page, page_size},
    timeout: 60000
    });
  return resp.data;
}

/**
 * Fetch gold/enriched data by silver or bronze id.
 * This will attempt multiple endpoints depending on what your backend exposes:
 * - GET /gold/:id
 * - GET /generate-story/:id (fallback)
 */
export async function fetchGoldById(id) {
  // Try gold first
  try {
    const resp = await axios.get(`${API_URL}/gold/${id}`, { timeout: 60000 });
    return resp.data;
  } catch (err) {
    // fallback to generate-story or gold?id query
    try {
      const resp2 = await axios.get(`${API_URL}/generate-story/${id}`, { timeout: 60000 });
      return resp2.data;
    } catch (err2) {
      // try query param
      const resp3 = await axios.get(`${API_URL}/gold?id=${encodeURIComponent(id)}`, { timeout: 60000 });
      return resp3.data;
    }
  }
}