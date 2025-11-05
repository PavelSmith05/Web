import { Navigate, createBrowserRouter, RouterProvider } from "react-router-dom";
import GradeDetailPage, {
  gradeDetailLoader,
} from "../pages/GradeDetailPage.tsx";
import GradesPage from "../pages/GradesPage.tsx";
import HomePage from "../pages/HomePage.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/grades",
    element: <GradesPage />,
  },
  {
    path: "/grades/:gradeId",
    loader: gradeDetailLoader,
    element: <GradeDetailPage />,
  },
  {
    path: "*",
    element: <Navigate to="/" replace />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
