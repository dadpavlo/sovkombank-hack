import { Link } from "react-router-dom"

const Missing = () => {
  return (
    <article style={{ padding: "100px" }}>
      <h1>Упс!</h1>
      <p>Страница не найдена</p>
      <div className="flexGrow">
        <Link to="/">На главную</Link>
      </div>
    </article>
  )
}

export default Missing
