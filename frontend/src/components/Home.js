import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthProvider";

const Home = () => {
  const { setAuth } = useContext(AuthContext);
  const navigate = useNavigate();

  const logout = async () => {
    setAuth({});
    navigate('/linkpage');
  }

  return (
    <section>
      <h1>Главная</h1>
      <br />
      <p>Вы вошли!</p>
      <br />
      <div className="flexGrow">
        <button onClick={logout}>Выйти</button>
      </div>
    </section>
  )
}

export default Home
