// src/pages/Login.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

export default function Login() {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Сохраняем токен или флаг авторизации (например, в localStorage)
        localStorage.setItem('isAuthenticated', 'true');
        navigate('/');
      } else {
        const err = await response.json();
        setError(err.detail || 'Неверный логин или пароль');
      }
    } catch (err) {
      console.error(err);
      setError('Не удалось подключиться к серверу');
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Вход</h1>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Логин"
          value={formData.username}
          onChange={handleChange}
          required
          className="input-field"
        />

        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={handleChange}
          required
          className="input-field"
        />

        <button type="submit" className="submit-button">
          Войти
        </button>
      </form>
    </div>
  );
}