import { useRef, useState, useEffect } from "react";
import { faCheck, faTimes, faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from '../api/axios';
import { Link } from "react-router-dom";

const USER_REGEX = /^[A-z][A-z0-9-_]{3,23}$/;
const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,24}$/;
const REGISTER_URL = '/signUp';

const Register = () => {
  const userRef = useRef();
  const errRef = useRef();

  const [login, setLogin] = useState('');
  const [validName, setValidName] = useState(false);
  const [userFocus, setUserFocus] = useState(false);

  const [password, setPassword] = useState('');
  const [validPassword, setValidPassword] = useState(false);
  const [passwordFocus, setPasswordFocus] = useState(false);

  const [matchPassword, setMatchPassword] = useState('');
  const [validMatch, setValidMatch] = useState(false);
  const [matchFocus, setMatchFocus] = useState(false);

  const [errMsg, setErrMsg] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    userRef.current.focus();
  }, [])

  useEffect(() => {
    setValidName(USER_REGEX.test(login));
  }, [login])

  useEffect(() => {
    setValidPassword(PWD_REGEX.test(password));
    setValidMatch(password === matchPassword);
  }, [password, matchPassword])

  useEffect(() => {
    setErrMsg('');
  }, [login, password, matchPassword])

  const handleSubmit = async (e) => {
    e.preventDefault();

    const v1 = USER_REGEX.test(login);
    const v2 = PWD_REGEX.test(password);
    if (!v1 || !v2) {
      setErrMsg("Invalid Entry");
      return;
    }
    try {
      const response = await axios.post(REGISTER_URL,
        JSON.stringify({ login, password }),
        {
          headers: { 'Content-Type': 'application/json' },
          withCredentials: true
        }
      );

      console.log(JSON.stringify(response?.data));

      setSuccess(true);

      setLogin('');
      setPassword('');
      setMatchPassword('');
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response');
      } else if (err.response?.status === 409) {
        setErrMsg('Username Taken');
      } else {
        setErrMsg('Registration Failed')
      }
      errRef.current.focus();
    }
  }

  return (
    <>
      {success ? (
        <section>
          <h1>Success!</h1>
          <p>
            <a href="#">Sign In</a>
          </p>
        </section>
      ) : (
        <section>
          <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
          <h1>Регистрация</h1>
          <form onSubmit={handleSubmit}>
            <label htmlFor="username">
              Имя пользователя:
              <FontAwesomeIcon icon={faCheck} className={validName ? "valid" : "hide"} />
              <FontAwesomeIcon icon={faTimes} className={validName || !login ? "hide" : "invalid"} />
            </label>
            <input
              type="text"
              id="username"
              ref={userRef}
              autoComplete="off"
              onChange={(e) => setLogin(e.target.value)}
              value={login}
              required
              aria-invalid={validName ? "false" : "true"}
              aria-describedby="uidnote"
              onFocus={() => setUserFocus(true)}
              onBlur={() => setUserFocus(false)}
            />
            <p id="uidnote" className={userFocus && login && !validName ? "instructions" : "offscreen"}>
              <FontAwesomeIcon icon={faInfoCircle} />
              от 4 до 24 символов.<br />
              Допускаются буквы, цифры, подчеркивания, дефисы.
            </p>


            <label htmlFor="password">
              Пароль:
              <FontAwesomeIcon icon={faCheck} className={validPassword ? "valid" : "hide"} />
              <FontAwesomeIcon icon={faTimes} className={validPassword || !password ? "hide" : "invalid"} />
            </label>
            <input
              type="password"
              id="password"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
              required
              aria-invalid={validPassword ? "false" : "true"}
              aria-describedby="pwdnote"
              onFocus={() => setPasswordFocus(true)}
              onBlur={() => setPasswordFocus(false)}
            />
            <p id="pwdnote" className={passwordFocus && !validPassword ? "instructions" : "offscreen"}>
              <FontAwesomeIcon icon={faInfoCircle} />
              от 8 до 24 символов.<br />
              Должны включать прописные и строчные буквы, цифру.
            </p>


            <label htmlFor="confirm_pwd">
              Повторите пароль:
              <FontAwesomeIcon icon={faCheck} className={validMatch && matchPassword ? "valid" : "hide"} />
              <FontAwesomeIcon icon={faTimes} className={validMatch || !matchPassword ? "hide" : "invalid"} />
            </label>
            <input
              type="password"
              id="confirm_pwd"
              onChange={(e) => setMatchPassword(e.target.value)}
              value={matchPassword}
              required
              aria-invalid={validMatch ? "false" : "true"}
              aria-describedby="confirmnote"
              onFocus={() => setMatchFocus(true)}
              onBlur={() => setMatchFocus(false)}
            />
            <p id="confirmnote" className={matchFocus && !validMatch ? "instructions" : "offscreen"}>
              <FontAwesomeIcon icon={faInfoCircle} />
              Должен совпадать с первым полем ввода пароля.
            </p>

            <button disabled={!validName || !validPassword || !validMatch ? true : false}>Зарегистрироваться</button>
          </form>
          <p>
            Уже зарегистрированы?<br />
            <span className="line">
              <Link to="/">Войти</Link>
            </span>
          </p>
        </section>
      )}
    </>
  )
}

export default Register
