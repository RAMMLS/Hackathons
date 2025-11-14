// src/App.js
import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Home />} />
    </Routes>
  );
}

export default App;
/*
const response = await fetch("/auth", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username: "john", password: "123" })
});

if (response.ok) {
  const data = await response.json();
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("username", data.username);
  
  // Переход на другую страницу
  window.location.href = "/dashboard"; // или router.push("/dashboard") в React/Vue
} else {
  alert("Ошибка авторизации");
}
*/
