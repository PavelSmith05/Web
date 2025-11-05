const rubleFormatter = new Intl.NumberFormat("ru-RU", {
  style: "currency",
  currency: "RUB",
  maximumFractionDigits: 0,
});

export function formatRubles(value?: number): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "—";
  }
  return rubleFormatter.format(value);
}

export function formatDate(value?: string): string {
  if (!value) {
    return "Не указана";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "Не указана";
  }
  return date.toLocaleDateString("ru-RU");
}

