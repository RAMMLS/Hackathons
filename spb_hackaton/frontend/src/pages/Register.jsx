// src/pages/Register.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

export default function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (error) setError(''); // сброс ошибки при изменении
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Валидация на клиенте
    if (formData.password !== formData.confirmPassword) {
      setError('Пароли не совпадают');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password
        })
      });

      if (response.ok) {
        localStorage.setItem('isAuthenticated', 'true');
        navigate('/');
      } else {
        const err = await response.json();
        setError(err.detail || 'Ошибка регистрации');
      }
    } catch (err) {
      console.error(err);
      setError('Не удалось подключиться к серверу');
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Регистрация</h1>

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

        <input
          type="password"
          name="confirmPassword"
          placeholder="Повторите пароль"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          className="input-field"
        />

        <button type="submit" className="submit-button">
          Подтвердить
        </button>
      </form>
    </div>
  );
}