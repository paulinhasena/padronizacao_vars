const API_BASE_URL = "http://localhost:8000";

export async function normalizeText({ text, outputFormat, useAi }) {
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
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail || "Erro ao processar solicitação.");
  }

  return response.json();
}
