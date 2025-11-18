import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './MainWindow.css';

const MainWindow = ({ onLogout, onStartGame, userName: propUserName }) => {
  const [isChatFullscreen, setIsChatFullscreen] = useState(false);
  const navigate = useNavigate();
  // Get username from prop, localStorage, or default
  const userName = propUserName || localStorage.getItem('username') || 'Пользователь';
  const [chatMessage, setChatMessage] = useState('');
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Привет! Я нейросеть-помощник на базе Mistral AI. Чем могу помочь?' }
  ]);
  const [userRating, setUserRating] = useState(150);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Доступные маскоты (12 вариантов)
  const mascots = [
    { src: '/moscot/first/1.png', name: 'Счастливый', status: 'Маскот готов помочь! Привет!' },
    { src: '/moscot/first/2.png', name: 'Удивленный', status: 'Вау! Это потрясающе!' },
    { src: '/moscot/first/3.png', name: 'Радостный', status: 'Отлично! Продолжайте в том же духе!' },
    { src: '/moscot/first/4.png', name: 'Злой', status: 'Хм, нужно подумать...' },
    { src: '/moscot/first/5.png', name: 'Смеющийся', status: 'Ха-ха! Это весело!' },
    { src: '/moscot/first/6.png', name: 'Дружелюбный', status: 'Привет! Давайте дружить!' },
    { src: '/moscot/second/1.png', name: 'Игривый', status: 'Давайте играть и учиться!' },
    { src: '/moscot/second/2.png', name: 'Любящий', status: 'Я вас люблю! Вы лучшие!' },
    { src: '/moscot/second/3.png', name: 'Грустный', status: 'Ой, не расстраивайтесь...' },
    { src: '/moscot/second/4.png', name: 'Поющий', status: 'Ла-ла-ла! Музыка вдохновляет!' },
    { src: '/moscot/second/5.png', name: 'Спящий', status: 'Zzz... Время для отдыха...' },
    { src: '/moscot/second/6.png', name: 'Подмигивающий', status: 'Все будет хорошо! Я уверен!' },
  ];

  // Загружаем сохраненный выбор маскота из localStorage
  const [mascotIndex, setMascotIndex] = useState(() => {
    const saved = localStorage.getItem('mascotIndex');
    return saved ? parseInt(saved, 10) : 0;
  });

  // Сохраняем выбор маскота в localStorage
  const handleMascotChange = (index) => {
    setMascotIndex(index);
    localStorage.setItem('mascotIndex', index.toString());
  };

  // Автоматическая прокрутка к новым сообщениям
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim() || isLoading) return;

    const userMessage = chatMessage.trim();
    
    // Добавляем сообщение пользователя
    const userMsg = { type: 'user', text: userMessage };
    setMessages(prev => [...prev, userMsg]);
    setChatMessage('');
    setIsLoading(true);

    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          model: 'mistral-small'
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Ошибка сервера' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botResponse = data.response || 'Извините, не удалось получить ответ.';
      
      setMessages(prev => [...prev, { type: 'bot', text: botResponse }]);
    } catch (error) {
      console.error('Ошибка при отправке сообщения:', error);
      const errorMessage = error.message.includes('Failed to fetch') || error.message.includes('ERR_EMPTY_RESPONSE')
        ? 'Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен.'
        : error.message || 'Произошла ошибка при обработке запроса.';
      
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: `Извините, произошла ошибка: ${errorMessage}` 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('access_token');
    if (onLogout) {
      onLogout();
    } else {
      navigate('/login');
    }
  };

  const handleStartGame = () => {
    if (onStartGame) {
      onStartGame();
    } else {
      navigate('/game');
    }
  };

  const quickActions = [
    { label: 'Учебные игры', action: handleStartGame },
    { label: 'База знаний', action: () => navigate('/articles') },
    { label: 'Мой профиль', action: () => navigate('/profile') },
  ];

  return (
    <div className="main-menu-container">
      {/* Header */}
      <header className="main-menu-header">
        <div className="app-title">Учебная платформа</div>
        <button className="logout-btn" onClick={handleLogout}>
          Выйти
        </button>
      </header>

          {isChatFullscreen ? (
      /* === ПОЛНОЭКРАННЫЙ ЧАТ === */
      <div className="chat-fullscreen-container">
        <div className="chat-fullscreen-header">
          <button
            className="back-btn action-btn"
            onClick={() => setIsChatFullscreen(false)}
          >
            ← Назад к меню
          </button>
          <div className="chat-status online">Online</div>
        </div>

        <div className="chat-fullscreen-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-avatar">
                {message.type === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <div className="message-text">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({ node, ...props }) => <p style={{ margin: 0 }} {...props} />,
                      a: ({ node, ...props }) => (
                        <a
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{ color: '#667eea', textDecoration: 'underline' }}
                          {...props}
                        />
                      ),
                      code: ({ node, inline, ...props }) => (
                        <code
                          style={{
                            background: 'rgba(0, 0, 0, 0.05)',
                            padding: inline ? '2px 4px' : '8px',
                            borderRadius: '4px',
                            fontSize: '0.9em',
                            fontFamily: 'monospace',
                            display: inline ? 'inline' : 'block',
                            margin: inline ? 0 : '4px 0',
                          }}
                          {...props}
                        />
                      ),
                      ul: ({ node, ...props }) => (
                        <ul style={{ margin: '4px 0', paddingLeft: '20px' }} {...props} />
                      ),
                      ol: ({ node, ...props }) => (
                        <ol style={{ margin: '4px 0', paddingLeft: '20px' }} {...props} />
                      ),
                      li: ({ node, ...props }) => (
                        <li style={{ margin: '2px 0' }} {...props} />
                      ),
                    }}
                  >
                    {message.text}
                  </ReactMarkdown>
                </div>
                <div className="message-time">
                  {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message bot-message">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="message-text typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-fullscreen-input-form" onSubmit={handleSendMessage}>
          <div className="input-container">
            <input
              type="text"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder={isLoading ? "Нейросеть думает..." : "Задайте вопрос..."}
              className="message-input"
              disabled={isLoading}
            />
            <button type="submit" className="send-button" disabled={isLoading}>
              {isLoading ? '⏳' : '📤'}
            </button>
          </div>
        </form>
      </div>
    ) : (
      /* === ОБЫЧНЫЙ РЕЖИМ (ТРИ ПАНЕЛИ) === */
      <div className="main-menu-content">
        {/* Левая панель - Кнопки и информация */}
        <div className="left-panel">
          <div className="quick-actions">
            <h3>Быстрые действия</h3>
            {quickActions.map((action, index) => (
              <button
                key={index}
                className="action-btn"
                onClick={action.action}
              >
                {action.label}
              </button>
            ))}
          </div>

          <div className="user-info-card">
            <div className="user-avatar">
              {userName?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="user-details">
              <div className="user-name">{userName || 'Пользователь'}</div>
              <div className="user-rating">
                <span className="rating-label">Рейтинг:</span>
                <span className="rating-value">{userRating}</span>
              </div>
            </div>
          </div>

          <div className="info-section">
            <h3>Полезная информация</h3>
            <div className="info-cards">
              <div className="info-card">
                <h4>Советы по обучению</h4>
                <p>• Регулярно занимайтесь</p>
                <p>• Используйте игры для практики</p>
                <p>• Отслеживайте прогресс</p>
              </div>
              <div className="info-card">
                <h4>Ваш прогресс</h4>
                <p>• Пройдено игр: 12</p>
                <p>• Средний балл: 85%</p>
                <p>• Активные дни: 15</p>
              </div>
            </div>
          </div>
        </div>

        {/* Центральная панель - Маскот */}
        <div className="center-panel">
          <div className="mascot-section">
            <div className="mascot-wrapper">
              <div className="mascot-container">
                <img 
                  src={mascots[mascotIndex].src} 
                  alt={mascots[mascotIndex].name}
                  className="mascot-image"
                />
                <div className="mascot-status">
                  <span className="status-text">{mascots[mascotIndex].status}</span>
                </div>
              </div>
            </div>
            <div className="mascot-controls">
              <div className="mascot-selector">
                <label className="mascot-select-label">Выберите маскота:</label>
              </div>
              <div className="mascot-buttons">
                {mascots.map((mascot, index) => (
                  <button
                    key={index}
                    className={`mascot-button ${mascotIndex === index ? 'active' : ''}`}
                    onClick={() => handleMascotChange(index)}
                    title={mascot.name}
                  >
                    <img 
                      src={mascot.src} 
                      alt={mascot.name}
                      className="mascot-button-image"
                    />
                  </button>
                ))}
              </div>
            </div>
            <div className="mascot-description">
              <p>Маскот меняется в зависимости от ваших успехов в обучении и настроения</p>
            </div>
          </div>
        </div>

        {/* Правая панель - Чат с нейросетью */}
        <div className="right-panel">
          <div className="chat-section">
            <div className="chat-header">
              <h3>Чат с нейросетью</h3>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <div className="chat-status online">Online</div>
                <button
                  className="fullscreen-toggle-btn"
                  onClick={() => setIsChatFullscreen(true)}
                  title="Развернуть чат"
                >
                  ⤢
                </button>
              </div>
            </div>
            
            <div className="chat-messages">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
                >
                  <div className="message-avatar">
                    {message.type === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <div className="message-text">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          p: ({ node, ...props }) => <p style={{ margin: 0 }} {...props} />,
                          a: ({ node, ...props }) => (
                            <a
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{ color: '#667eea', textDecoration: 'underline' }}
                              {...props}
                            />
                          ),
                          code: ({ node, inline, ...props }) => (
                            <code
                              style={{
                                background: 'rgba(0, 0, 0, 0.05)',
                                padding: inline ? '2px 4px' : '8px',
                                borderRadius: '4px',
                                fontSize: '0.9em',
                                fontFamily: 'monospace',
                                display: inline ? 'inline' : 'block',
                                margin: inline ? 0 : '4px 0',
                              }}
                              {...props}
                            />
                          ),
                          ul: ({ node, ...props }) => (
                            <ul style={{ margin: '4px 0', paddingLeft: '20px' }} {...props} />
                          ),
                          ol: ({ node, ...props }) => (
                            <ol style={{ margin: '4px 0', paddingLeft: '20px' }} {...props} />
                          ),
                          li: ({ node, ...props }) => (
                            <li style={{ margin: '2px 0' }} {...props} />
                          ),
                        }}
                      >
                        {message.text}
                      </ReactMarkdown>
                    </div>
                    <div className="message-time">
                      {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message bot-message">
                  <div className="message-avatar">🤖</div>
                  <div className="message-content">
                    <div className="message-text typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form className="chat-input-form" onSubmit={handleSendMessage}>
              <div className="input-container">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  placeholder={isLoading ? "Нейросеть думает..." : "Задайте вопрос нейросети..."}
                  className="message-input"
                  disabled={isLoading}
                />
                <button type="submit" className="send-button" disabled={isLoading}>
                  {isLoading ? '⏳' : '📤'}
                </button>
              </div>
            </form>
          </div>

          <div className="leaderboard-section">
            <h3>Топ игроков</h3>
            <div className="leaderboard">
              <div className="leaderboard-item current">
                <span className="rank">1</span>
                <span className="name">{userName || 'Вы'}</span>
                <span className="score">{userRating}</span>
              </div>
              <div className="leaderboard-item">
                <span className="rank">2</span>
                <span className="name">Alex</span>
                <span className="score">145</span>
              </div>
              <div className="leaderboard-item">
                <span className="rank">3</span>
                <span className="name">Maria</span>
                <span className="score">132</span>
              </div>
              <div className="leaderboard-item">
                <span className="rank">4</span>
                <span className="name">John</span>
                <span className="score">128</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    )}
    </div>
  );
};

export default MainWindow;

