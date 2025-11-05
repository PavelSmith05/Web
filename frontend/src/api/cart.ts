import type { DataSource } from "../types/api.ts";

export interface CartSummary {
  calculationId: number | null;
  itemCount: number;
  source: DataSource;
}

interface CartDto {
  id?: number | null;
  count?: number;
}

const FALLBACK: CartSummary = {
  calculationId: null,
  itemCount: 0,
  source: "mock",
};

export async function fetchCartSummary(): Promise<CartSummary> {
  try {
    const response = await fetch("/api/cart/", { credentials: "include" });
    if (!response.ok) {
      throw new Error(`API responded with ${response.status}`);
    }
    const payload = (await response.json()) as CartDto;
    return {
      calculationId: payload.id === undefined || payload.id === null || payload.id < 0 ? null : payload.id,
      itemCount: payload.count ?? 0,
      source: "api",
    };
  } catch (error) {
    console.warn("[fetchCartSummary] fallback to mock data:", error);
    return FALLBACK;
  }
}

