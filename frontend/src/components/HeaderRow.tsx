import { Link } from "react-router-dom";
import { MINIO_PUBLIC_BASE_URL } from "../config/env.ts";

interface HeaderRowProps {
  title?: string;
}

const DEFAULT_TITLE = "Рассчёт прочности бетонной балки на изгиб";

function HeaderRow({ title = DEFAULT_TITLE }: HeaderRowProps) {
  return (
    <div className="list-header-row">
      <Link to="/" className="list-logo-link" aria-label="Перейти на главную">
        <div
          className="list-logo"
          style={{
            backgroundImage: `url('${MINIO_PUBLIC_BASE_URL}logo.png')`,
          }}
        />
      </Link>
      <div className="list-title">{title}</div>
    </div>
  );
}

export default HeaderRow;

