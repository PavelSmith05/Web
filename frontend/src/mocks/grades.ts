import { MINIO_PUBLIC_BASE_URL } from "../config/env.ts";
import type { ConcreteGrade } from "../types/grade.ts";

export const mockGrades: ConcreteGrade[] = [
  {
    id: 1,
    code: "M100",
    name: "M100",
    description: "Дешевый и хрупкий.",
    compressiveStrengthMpa: 10,
    pricePerCubicMeter: 3800,
    imageUrl: `${MINIO_PUBLIC_BASE_URL}m100.jpg`,
  },
  {
    id: 2,
    code: "М150",
    name: "М150",
    description: "Недорогой и практичный.",
    compressiveStrengthMpa: 15,
    pricePerCubicMeter: 4200,
    imageUrl: `${MINIO_PUBLIC_BASE_URL}m150.jpg`,
  },
  {
    id: 3,
    code: "М200",
    name: "М200",
    description: "Надежный и популярный.",
    compressiveStrengthMpa: 20,
    pricePerCubicMeter: 4600,
    imageUrl: `${MINIO_PUBLIC_BASE_URL}m200.jpg`,
  },
  {
    id: 4,
    code: "М250",
    name: "М250",
    description: "Универсальный и крепкий.",
    compressiveStrengthMpa: 25,
    pricePerCubicMeter: 5100,
    imageUrl: `${MINIO_PUBLIC_BASE_URL}m250.jpg`,
  },
  {
    id: 5,
    code: "M300",
    name: "M300",
    description: "Прочный и долговечный.",
    compressiveStrengthMpa: 30,
    pricePerCubicMeter: 5600,
    imageUrl: `${MINIO_PUBLIC_BASE_URL}m300.jpg`,
  },
];

export function filterMockGrades(params: {
  name?: string;
  strengthMin?: number;
  strengthMax?: number;
}): ConcreteGrade[] {
  return mockGrades.filter((grade) => {
    if (params.name) {
      const query = params.name.toLowerCase();
      const matchesName =
        grade.name.toLowerCase().includes(query) ||
        grade.code.toLowerCase().includes(query);
      if (!matchesName) {
        return false;
      }
    }

    if (
      typeof params.strengthMin === "number" &&
      grade.compressiveStrengthMpa < params.strengthMin
    ) {
      return false;
    }
    if (
      typeof params.strengthMax === "number" &&
      grade.compressiveStrengthMpa > params.strengthMax
    ) {
      return false;
    }

    return true;
  });
}
