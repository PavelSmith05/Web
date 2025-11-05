import { MINIO_PUBLIC_BASE_URL } from "../config/env.ts";
import { filterMockGrades, mockGrades } from "../mocks/grades.ts";
import type { FetchResult } from "../types/api.ts";
import type { ConcreteGrade, ConcreteGradeDto } from "../types/grade.ts";

export interface GradeFilters {
  name?: string;
  strengthMin?: number;
  strengthMax?: number;
}

function buildImageUrl(dto: ConcreteGradeDto): string | undefined {
  if (dto.image_url) {
    return dto.image_url;
  }
  if (dto.image_key) {
    return `${MINIO_PUBLIC_BASE_URL}${dto.image_key}`;
  }
  return undefined;
}

function mapGrade(dto: ConcreteGradeDto): ConcreteGrade {
  return {
    id: dto.id,
    code: dto.grade_code,
    name: dto.name,
    description: dto.description ?? "Описание недоступно",
    compressiveStrengthMpa: dto.compressive_strength_mpa,
    pricePerCubicMeter: dto.price_per_m3_rub,
    imageUrl: buildImageUrl(dto),
    certifiedAt: dto.certified_at ?? undefined,
  };
}

function prepareQuery(filters: GradeFilters): URLSearchParams {
  const params = new URLSearchParams();
  if (filters.name) {
    params.set("grade_search", filters.name);
  }
  if (typeof filters.strengthMin === "number") {
    params.set("strength_min", filters.strengthMin.toString());
  }
  if (typeof filters.strengthMax === "number") {
    params.set("strength_max", filters.strengthMax.toString());
  }
  return params;
}

export async function fetchGrades(
  filters: GradeFilters,
): Promise<FetchResult<ConcreteGrade[]>> {
  const params = prepareQuery(filters);
  let requestUrl = "/api/grades/";
  const queryString = params.toString();
  if (queryString) {
    requestUrl += `?${queryString}`;
  }

  try {
    const response = await fetch(requestUrl, { credentials: "include" });
    if (!response.ok) {
      throw new Error(`API responded with ${response.status}`);
    }
    const payload = (await response.json()) as ConcreteGradeDto[];
    return {
      data: payload.map(mapGrade),
      source: "api",
    };
  } catch (error) {
    console.warn("[fetchGrades] fallback to mock data:", error);
    return {
      data: filterMockGrades(filters),
      source: "mock",
    };
  }
}

export async function fetchGradeById(
  id: number,
): Promise<FetchResult<ConcreteGrade>> {
  try {
    const response = await fetch(`/api/grades/${id}/`, {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error(`API responded with ${response.status}`);
    }
    const payload = (await response.json()) as ConcreteGradeDto;
    return {
      data: mapGrade(payload),
      source: "api",
    };
  } catch (error) {
    console.warn("[fetchGradeById] fallback to mock data:", error);
    const fallback = mockGrades.find((grade) => grade.id === id);
    if (!fallback) {
      throw new Error("Grade not found in mock data");
    }
    return {
      data: fallback,
      source: "mock",
    };
  }
}

