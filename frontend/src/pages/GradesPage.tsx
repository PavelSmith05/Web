import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useSearchParams } from "react-router-dom";
import { fetchGrades } from "../api/grades.ts";
import { fetchCartSummary } from "../api/cart.ts";
import GradeCard from "../components/grades/GradeCard.tsx";
import HeaderRow from "../components/HeaderRow.tsx";
import type { GradeFilters } from "../api/grades.ts";
import type { ConcreteGrade } from "../types/grade.ts";

interface GradeFiltersFormValues {
  name: string;
}

function formValuesFromParams(params: URLSearchParams): GradeFiltersFormValues {
  return {
    name: params.get("name") ?? "",
  };
}

function sanitizeFilters(values: GradeFiltersFormValues): GradeFilters {
  return {
    name: values.name.trim() || undefined,
  };
}

function GradesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [formValues, setFormValues] = useState<GradeFiltersFormValues>(() =>
    formValuesFromParams(searchParams),
  );
  const [grades, setGrades] = useState<ConcreteGrade[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dataSource, setDataSource] = useState<"api" | "mock">("api");
  const [cart, setCart] = useState<{ calcId: number | null; count: number }>(
    () => ({ calcId: null, count: 0 }),
  );

  const filters = useMemo(
    () => sanitizeFilters(formValuesFromParams(searchParams)),
    [searchParams],
  );

  useEffect(() => {
    setFormValues(formValuesFromParams(searchParams));
  }, [searchParams]);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError(null);
    fetchGrades(filters)
      .then((result) => {
        if (!isMounted) return;
        setGrades(result.data);
        setDataSource(result.source);
      })
      .catch((err: Error) => {
        if (!isMounted) return;
        setError(err.message);
        setGrades([]);
      })
      .finally(() => {
        if (!isMounted) return;
        setLoading(false);
      });
    return () => {
      isMounted = false;
    };
  }, [filters]);

  useEffect(() => {
    fetchCartSummary().then((summary) => {
      setCart({ calcId: summary.calculationId, count: summary.itemCount });
    });
  }, []);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const params = new URLSearchParams();
    if (formValues.name) {
      params.set("name", formValues.name);
    }
    setSearchParams(params);
  };

  const handleAddClick = () => {
    window.alert("Добавление в заявку доступно после авторизации в основной системе.");
  };

  return (
    <div
      className="list-frame"
      data-calc-id={cart.calcId ?? undefined}
      data-cart-count={cart.count}
    >
      <div className="list-header-bar"></div>
      <HeaderRow />
      <a
        href={cart.calcId ? `/beam-calculation/${cart.calcId}/` : "#"}
        className="cart-button"
        title={cart.calcId ? "Открыть черновик" : "Пока нет черновика расчёта"}
      >
        <div className="cart-icon">🛒</div>
        <div className="cart-count">{cart.count}</div>
      </a>

      <form className="list-filters-form" onSubmit={handleSubmit}>
        <input
          className="list-search-input"
          type="text"
          name="grade_search"
          value={formValues.name}
          placeholder="Введите марку бетона..."
        onChange={(event) => {
          const { value } = event.currentTarget;
          setFormValues((prev) => ({ ...prev, name: value }));
        }}
        />
        <button className="list-search-button" type="submit" disabled={loading}>
          Найти
        </button>
      </form>

      {loading && <div className="list-status list-status--loading">Загрузка...</div>}
      {error && (
        <div className="list-status list-status--error">
          Не удалось загрузить данные: {error}
        </div>
      )}
      {!loading && !error && dataSource === "mock" && (
        <div className="list-status list-status--warning">
          Показаны mock-данные: сервер временно недоступен.
        </div>
      )}

      <div className="list-cards-grid">
        {!loading && !error && grades.length === 0 ? (
          <div className="no-results">По вашему запросу ничего не найдено</div>
        ) : (
          grades.map((grade, index) => (
            <GradeCard
              key={grade.id}
              grade={grade}
              index={index}
              onAdd={handleAddClick}
            />
          ))
        )}
      </div>
    </div>
  );
}

export default GradesPage;

