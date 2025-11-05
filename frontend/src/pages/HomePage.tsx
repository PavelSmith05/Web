import { Link } from "react-router-dom";
import HeaderRow from "../components/HeaderRow.tsx";
import { MINIO_PUBLIC_BASE_URL } from "../config/env.ts";

function HomePage() {
  return (
    <div className="home-frame" data-page="home">
      <div className="list-header-bar"></div>
      <HeaderRow />
      <div className="home-card">
        <div
          className="home-card-logo"
          style={{ backgroundImage: `url('${MINIO_PUBLIC_BASE_URL}logo.png')` }}
        ></div>
        <div className="home-card-content">
          <h1 className="home-card-title">Flexural Concrete</h1>
          <p className="home-card-text">
            Сервис подбора марок бетона для расчёта прочности изгибаемых
            железобетонных балок.
          </p>
          <p className="home-card-text">
            Используйте раздел «Каталог марок» для поиска подходящих
            бетонных смесей по названию и характеристикам прочности.
          </p>
          <ul className="home-card-list">
            <li>Каталог марок бетона с характеристиками;</li>
            <li>Поиск и фильтрация по параметрам;</li>
            <li>Детальная информация о каждой марке;</li>
            <li>Интеграция с расчётной системой.</li>
          </ul>
          <Link to="/grades" className="home-next-button">
            Далее
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
