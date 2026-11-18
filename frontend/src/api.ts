import type { AnalyzeResponse } from "./types";

export const API_BASE = "http://127.0.0.1:8001";

async function readError(response: Response): Promise<string> {
  try {
    const data: { detail?: string | { msg?: string }[] } = await response.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) {
      return data.detail.map((item) => item.msg ?? "Invalid input").join(", ");
    }
    return `Request failed (${response.status})`;
  } catch {
    return `Request failed (${response.status})`;
  }
}

export async function analyzeOutfit(file: File): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("file", file);

  let response: Response;
  try {
    response = await fetch(`${API_BASE}/outfits/analyze`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "Could not reach the server. Make sure the backend is running on port 8001.",
    );
  }

  if (!response.ok) throw new Error(await readError(response));
  return (await response.json()) as AnalyzeResponse;
}