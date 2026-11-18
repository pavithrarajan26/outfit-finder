export type OutfitItem = {
  id: string;
  category: string;
  color: string;
  style: string;
  description: string;
  search_query: string;
  confidence: number;
};

export type AnalyzeResponse = {
  items: OutfitItem[];
  source: string; // "mock" or "claude"
};