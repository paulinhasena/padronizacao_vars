import { useState } from "react";
import { normalizeFile, normalizeText } from "./api.js";
import { Header } from "./components/Header.jsx";
import { InputPanel } from "./components/InputPanel.jsx";
import { ResultPanel } from "./components/ResultPanel.jsx";

export default function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [outputFormat, setOutputFormat] = useState("all");
  const [useAi, setUseAi] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit() {
    setLoading(true);
    setError("");

    try {
      if (!file && !text.trim()) {
        throw new Error("Informe variáveis por texto ou envie um arquivo CSV/Excel.");
      }

      const payload = file
        ? await normalizeFile({ file, outputFormat, useAi })
        : await normalizeText({ text, outputFormat, useAi });

      setResult(payload);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <Header />

      <div className="container grid">
        <InputPanel
          text={text}
          setText={setText}
          file={file}
          setFile={setFile}
          outputFormat={outputFormat}
          setOutputFormat={setOutputFormat}
          useAi={useAi}
          setUseAi={setUseAi}
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
        />

        <ResultPanel result={result} />
      </div>
    </main>
  );
}
