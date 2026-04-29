import { useMemo, useState } from "react";
import { CheckCircle2, Copy, Table2 } from "lucide-react";
import { ResultTable } from "./ResultTable.jsx";

export function ResultPanel({ result }) {
  const [activeTab, setActiveTab] = useState("table");
  const [copied, setCopied] = useState(false);

  const averageConfidence = useMemo(() => {
    if (!result?.results?.length) return 0;
    const total = result.results.reduce((sum, item) => sum + item.confidence, 0);
    return Math.round((total / result.results.length) * 100);
  }, [result]);

  if (!result) {
    return (
      <section className="card empty-card">
        <div className="empty-state">
          <div className="empty-icon">
            <Table2 size={34} />
          </div>
          <h2>Resultado aparecerá aqui</h2>
          <p>
            O retorno virá em tabela, terraform.tfvars e formato NoScript/NoCode.
          </p>
        </div>
      </section>
    );
  }

  const codeContent = activeTab === "tfvars" ? result.tfvars : result.noscript;

  async function copyCode() {
    if (!codeContent) return;
    await navigator.clipboard.writeText(codeContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 1400);
  }

  return (
    <section className="card">
      <div className="card-content">
        <div className="result-header">
          <div>
            <div className="section-kicker">
              <CheckCircle2 size={16} />
              Resultado
            </div>
            <h2 className="card-title">Saída pronta para revisão</h2>
            <p className="card-description">
              Use o retorno para modelagem, documentação, configuração e alinhamento técnico.
            </p>
          </div>
        </div>

        <div className="metric-grid">
          <div className="metric">
            <div className="metric-value">{result.results?.length || 0}</div>
            <div className="metric-label">variáveis processadas</div>
          </div>
          <div className="metric">
            <div className="metric-value">{averageConfidence}%</div>
            <div className="metric-label">confiança média</div>
          </div>
          <div className="metric">
            <div className="metric-value">3</div>
            <div className="metric-label">formatos gerados</div>
          </div>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === "table" ? "active" : ""}`}
            onClick={() => setActiveTab("table")}
          >
            Tabela
          </button>
          <button
            className={`tab ${activeTab === "tfvars" ? "active" : ""}`}
            onClick={() => setActiveTab("tfvars")}
          >
            terraform.tfvars
          </button>
          <button
            className={`tab ${activeTab === "noscript" ? "active" : ""}`}
            onClick={() => setActiveTab("noscript")}
          >
            NoScript/NoCode
          </button>

          {activeTab !== "table" ? (
            <button className="copy-button" onClick={copyCode}>
              <Copy size={15} />
              {copied ? "Copiado" : "Copiar"}
            </button>
          ) : null}
        </div>

        {activeTab === "table" ? (
          <ResultTable rows={result.table || result.results} />
        ) : (
          <pre className="code-block">{codeContent}</pre>
        )}
      </div>
    </section>
  );
}
