export type DataSource = "api" | "mock";

export interface FetchResult<T> {
  data: T;
  source: DataSource;
}

