import { useNavigate } from "react-router-dom"

const Unauthorized = () => {
  const navigate = useNavigate();

  const goBack = () => navigate(-1);

  return (
    <section>
      <p>У вас нет доступа к запрашиваемой странице.</p>
      <div className="flexGrow">
        <button onClick={goBack}>Назад</button>
      </div>
    </section>
  )
}

export default Unauthorized
