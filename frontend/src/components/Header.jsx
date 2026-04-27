import { BrainCircuit, DatabaseZap, Sparkles } from "lucide-react";

export function Header() {
  return (
    <header className="header">
      <div className="container header-grid">
        <div>
          <div className="badge">
            <Sparkles size={16} />
            Data Naming AI
          </div>

          <h1 className="title">
            Padronização inteligente de variáveis para engenharia de dados.
          </h1>

          <p className="subtitle">
            Um MVP com experiência simples para qualquer pessoa usar: cole variáveis,
            envie CSV/Excel e receba nomes lógicos, físicos, descrições e formatos
            prontos para modelagem, configuração e documentação.
          </p>
        </div>

        <div className="hero-card">
          <div className="hero-icon">
            <BrainCircuit size={30} />
          </div>
          <h3>IA aplicada ao fluxo real</h3>
          <p>
            Não é só automação. É governança, padronização, reuso e redução de esforço
            manual na rotina de dados.
          </p>

          <div className="hero-mini-card">
            <DatabaseZap size={18} />
            <span>Regras + dicionário + camada plugável de IA</span>
          </div>
        </div>
      </div>
    </header>
  );
}
