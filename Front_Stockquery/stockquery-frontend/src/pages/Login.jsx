import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../img/logo.png';           
import '../styles/login.css';                
import { loginUser } from '../api/auth';     
const Login = () => {
  const [correo, setCorreo] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!correo || !contraseña) {
      setErrorMessage('Por favor ingrese todos los campos');
      return;
    }

    try {
      const data = await loginUser(correo, contraseña);
      if (data.usuario) {
        localStorage.setItem('user', JSON.stringify(data.usuario));
        navigate('/dashboard');
      } else {
        setErrorMessage('Credenciales inválidas');
      }
    } catch (error) {
      console.error(error);
      setErrorMessage('Error al iniciar sesión');
    }
  };

  return (
    <>
      <div className="background-container"></div>

      <div className="login-container">
        <h1 className="login-title">LOGIN</h1>
        <div className="logo-container">
          <img src={logo} alt="StockQuery Logo" className="logo" />
        </div>
        <h2 className="app-title">StockQuery</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Correo</label>
            <input
              type="email"
              id="email"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              required
              placeholder="Ingrese su correo"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              value={contraseña}
              onChange={(e) => setContraseña(e.target.value)}
              required
              placeholder="Ingrese su contraseña"
            />
          </div>
          <button type="submit" className="login-button">Iniciar sesión</button>
        </form>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </div>
    </>
  );
};

export default Login;
