import type { MouseEventHandler } from "react";
import { Link } from "react-router-dom";
import type { ConcreteGrade } from "../../types/grade.ts";

interface GradeCardProps {
  grade: ConcreteGrade;
  index: number;
  onAdd?: MouseEventHandler<HTMLButtonElement>;
}

const PLACEHOLDER_SRC = "/grade-placeholder.svg";

function GradeCard({ grade, index, onAdd }: GradeCardProps) {
  const cardIndex = (index % 10) + 1;
  const image = grade.imageUrl ?? PLACEHOLDER_SRC;

  return (
    <div className={`list-card--${cardIndex}`}>
      <div className="list-card-bg"></div>
      <div
        className="list-card-image"
        style={{ backgroundImage: `url('${image}')` }}
      ></div>
      <div className="list-card-text">
        Марка бетона: {grade.name}
        <br />
        {grade.description}
        <br />
        Коэффициент прочности: {grade.compressiveStrengthMpa}
      </div>
      <div className="list-card-actions">
        <button type="button" className="list-card-btn" onClick={onAdd}>
          Добавить
        </button>
        <Link className="list-card-btn" to={`/grades/${grade.id}`}>
          Подробнее
        </Link>
      </div>
    </div>
  );
}

export default GradeCard;
