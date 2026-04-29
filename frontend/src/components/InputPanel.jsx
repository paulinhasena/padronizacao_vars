import { FileSpreadsheet, UploadCloud, Wand2 } from "lucide-react";

const example = `codigo identificacao - pessoa | Formato criptografado do id do cliente.
data nascimento cliente | Data de nascimento do cliente.
valor contrato credito | Valor total do contrato de crédito.
codigo matricula beneficio | Código da matrícula do benefício INSS.`;

export function InputPanel({
  text,
  setText,
  file,
  setFile,
  outputFormat,
  setOutputFormat,
  useAi,
  setUseAi,
  onSubmit,
  loading,
  error,
}) {
  return (
    <section className="card">
      <div className="card-content">
        <div className="section-kicker">
          <FileSpreadsheet size={16} />
          Entrada
        </div>

        <h2 className="card-title">Envie variáveis</h2>
        <p className="card-description">
          Use texto livre ou arquivo. Para melhores resultados, informe nome e descrição.
        </p>

        <div className="field">
          <label className="label">Copiar e colar</label>
          <textarea
            className="textarea"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder={example}
          />
        </div>

        <div className="field">
          <label className="label icon-label">
            <UploadCloud size={16} />
            Arquivo CSV ou Excel
          </label>
          <input
            className="file-input"
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={(event) => setFile(event.target.files?.[0] || null)}
          />
          {file ? <small className="hint">Selecionado: {file.name}</small> : null}
        </div>

        <div className="field">
          <label className="label">Formato de saída</label>
          <select
            className="select"
            value={outputFormat}
            onChange={(event) => setOutputFormat(event.target.value)}
          >
            <option value="all">Padrão — todas as opções</option>
            <option value="table">Tabela</option>
            <option value="tfvars">terraform.tfvars</option>
            <option value="noscript">NoScript/NoCode</option>
          </select>
        </div>

        <label className="toggle-row">
          <input
            className="checkbox"
            type="checkbox"
            checked={useAi}
            onChange={(event) => setUseAi(event.target.checked)}
          />
          <span>
            Usar camada de IA quando configurada
            <small>O MVP roda mesmo sem chave externa.</small>
          </span>
        </label>

        <button className="button" onClick={onSubmit} disabled={loading}>
          <Wand2 size={18} />
          {loading ? "Processando..." : "Padronizar variáveis"}
        </button>

        {error ? <div className="error">{error}</div> : null}
      </div>
    </section>
  );
}
