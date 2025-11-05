const DEFAULT_MINIO_BASE_URL = "http://localhost:9000/beam-images/";

export const MINIO_PUBLIC_BASE_URL =
  import.meta.env.VITE_MINIO_PUBLIC_BASE_URL ?? DEFAULT_MINIO_BASE_URL;

