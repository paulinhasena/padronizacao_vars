export function ResultTable({ rows }) {
  if (!rows?.length) {
    return null;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Original</th>
            <th>Nome lógico</th>
            <th>Nome físico</th>
            <th>Descrição</th>
            <th>Confiança</th>
            <th>Natureza</th>
            <th>Explicação</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((item, index) => (
            <tr key={`${item.physical_name}-${index}`}>
              <td>{item.original_name}</td>
              <td>{item.logical_name}</td>
              <td>
                <code className="inline-code">{item.physical_name}</code>
              </td>
              <td>{item.description}</td>
              <td>
                <span className={confidenceClass(item.confidence)}>
                  {Math.round(item.confidence * 100)}%
                </span>
              </td>
              <td>{item.nature}</td>
              <td>{item.explanation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function confidenceClass(confidence) {
  if (confidence >= 0.8) return "confidence high";
  if (confidence >= 0.5) return "confidence medium";
  return "confidence low";
}
