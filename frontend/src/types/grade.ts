export interface ConcreteGradeDto {
  id: number;
  grade_code: string;
  name: string;
  description?: string;
  compressive_strength_mpa: number;
  price_per_m3_rub?: number;
  image_key?: string | null;
  image_url?: string | null;
  status?: string;
  certified_at?: string | null;
}

export interface ConcreteGrade {
  id: number;
  code: string;
  name: string;
  description: string;
  compressiveStrengthMpa: number;
  pricePerCubicMeter?: number;
  imageUrl?: string;
  certifiedAt?: string;
}

