// Este arquivo concentra as chamadas do frontend para o backend.
//
// Em desenvolvimento:
// - frontend roda em http://localhost:5173
// - backend roda em http://localhost:8000
//
// Em modo corporativo:
// - frontend já está compilado em frontend/dist
// - backend serve a tela em http://localhost:8000
// - por isso usamos URL relativa.
const API_BASE_URL = import.meta.env.DEV ? "http://localhost:8000" : "";

export async function normalizeText({ text, outputFormat, useAi }) {
  // Monta um FormData porque o backend espera dados de formulário.
  const formData = new FormData();
  formData.append("text", text);
  formData.append("output_format", outputFormat);
  formData.append("use_ai", useAi);

  const response = await fetch(`${API_BASE_URL}/normalize/text`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

export async function normalizeFile({ file, outputFormat, useAi }) {
  // Envia arquivo CSV/Excel para o backend.
  const formData = new FormData();
  formData.append("file", file);
  formData.append("output_format", outputFormat);
  formData.append("use_ai", useAi);

  const response = await fetch(`${API_BASE_URL}/normalize/file`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

async function handleResponse(response) {
  // Se o backend retornar erro, exibimos uma mensagem amigável na tela.
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail || "Erro ao processar solicitação.");
  }

  return response.json();
}
