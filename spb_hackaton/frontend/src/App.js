import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
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
export default App;
