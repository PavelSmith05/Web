import { useLoaderData } from "react-router-dom";
import type { LoaderFunctionArgs } from "react-router-dom";
import HeaderRow from "../components/HeaderRow.tsx";
import { fetchGradeById } from "../api/grades.ts";
import type { FetchResult } from "../types/api.ts";
import type { ConcreteGrade } from "../types/grade.ts";
import { formatDate, formatRubles } from "../utils/format.ts";

const PLACEHOLDER_SRC = "/grade-placeholder.svg";

type LoaderResult = FetchResult<ConcreteGrade>;

export async function gradeDetailLoader({ params }: LoaderFunctionArgs) {
  const rawId = params.gradeId;
  const id = Number(rawId);
  if (!rawId || !Number.isInteger(id)) {
    throw new Response("Not found", { status: 404 });
  }
  try {
    const result = await fetchGradeById(id);
    return result satisfies LoaderResult;
  } catch (error) {
    throw new Response("Not found", { status: 404 });
  }
}

function GradeDetailPage() {
  const { data: grade } = useLoaderData() as LoaderResult;
  const image = grade.imageUrl ?? PLACEHOLDER_SRC;
  const priceText = formatRubles(grade.pricePerCubicMeter);
  const certifiedText = formatDate(grade.certifiedAt);

  return (
    <div className="detail-frame" data-grade-id={grade.id}>
      <div className="list-header-bar"></div>
      <HeaderRow />
      <div className="detail-card-wrap">
        <div className="detail-card-bg"></div>
        <div className="detail-card-title">Марка бетона: {grade.name}</div>
        <div
          className="detail-card-image"
          style={{ backgroundImage: `url('${image}')`, backgroundSize: "cover" }}
        ></div>
        <div className="detail-card-desc">
          {grade.description}
          <br />
          <strong>Коэффициент прочности:</strong> {grade.compressiveStrengthMpa}
          <br />
          <strong>Цена за м³:</strong> {priceText}
          <br />
          <strong>Сертификация:</strong> {certifiedText}
        </div>
        <button
          type="button"
          className="detail-card-btn"
          onClick={() => window.alert("Добавление доступно после авторизации.")}
        >
          Добавить
        </button>
      </div>
    </div>
  );
}

export default GradeDetailPage;
