import React, { useState } from "react";
import { uploadFile } from "../api";

export default function UploadForm({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus("");
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please choose a file to upload.");
      return;
    }
    setStatus("Uploading...");
    setError(null);
    try {
      const result = await uploadFile(file);
      setStatus("Upload successful");
      if (onUploaded) onUploaded(result);
    } catch (err) {
      console.error(err);
      setError(
        err?.response?.data?.message ||
          err?.message ||
          "Upload failed, check console for details"
      );
      setStatus("");
    }
  };

  return (
    <div className="p-4 border border-gray-200 rounded-md bg-white shadow-sm">
      <h3 className="text-lg font-semibold mb-3">Upload dataset</h3>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="file"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-700"
        />
        <div>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Upload
          </button>
        </div>
      </form>
      {status && <p className="mt-3 text-green-600">{status}</p>}
      {error && <p className="mt-3 text-red-600">{error}</p>}
    </div>
  );
}