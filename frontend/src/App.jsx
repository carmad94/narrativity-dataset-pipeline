import React, {useState} from "react";
import UploadForm from "./components/UploadForm";
import DatasetList from "./components/DatasetList";
import GoldViewer from "./components/GoldViewer";

export default function App() {
const [selectedId, setSelectedId] = useState(null);

  return (
    <div style={{ padding: 20, maxWidth: 1000, margin: "0 auto" }}>
      <h1 class="text-5xl font-extrabold text-gray-900 dark:text-white">Narrativity Score Dashboard</h1>
      <br/>
      <p>Upload narrativity scores and view AI-enriched explanation.</p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <UploadForm onUploaded={() => window.location.reload()} />
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 6 }}>
          <h3>Quick instructions</h3>
          <ol>
            <li>Use the Upload form to post a CSV/Excel to your backend <code>/upload</code> endpoint.</li>
            <li>After upload, records will be visible in the Bronze list. Click "View Gold" to see AI-enriched data.</li>
            <li>You can also open a gold record directly by visiting <code>/gold/&lt;id&gt;</code>.</li>
          </ol>
        </div>
      </div>

      <div className="flex relative">
        <div className="flex-1">
            <DatasetList onSelect={(id) => setSelectedId(id)} selectedId={selectedId}/>
        </div>

        {selectedId && (
            <div className="fixed inset-y-0 right-0 w-1/3 bg-white shadow-lg border-l border-gray-300 transform transition-transform duration-300 ease-in-out">
            <GoldViewer id={selectedId} onBack={() => setSelectedId(null)} />
            </div>
        )}
      </div>
    </div>
  );
}