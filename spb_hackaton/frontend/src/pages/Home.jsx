// src/pages/Home.jsx
import { useState } from 'react';
import '../App.css';
import ProfileForm from '../components/ProfileForm';
import ArticleDisplay from '../components/ArticleDisplay';
import './Home.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function Home() {
  const [article, setArticle] = useState(null);
  const [topics, setTopics] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleProfileSubmit = async (profileData) => {
    setIsLoading(true);
    setError(null);
    setArticle(null);
    setTopics(null);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 360000); // 6 minutes timeout (model loading can take time)

      const response = await fetch(`${API_BASE_URL}/api/v1/profile/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Check if response is empty
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        if (response.status === 0 || response.statusText === '') {
          throw new Error('Empty response from server. The backend may have crashed. Check backend logs: docker-compose logs backend');
        }
      }

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          // If we can't parse JSON, try to get text
          try {
            const text = await response.text();
            if (text) errorMessage = text.substring(0, 200);
          } catch (e2) {
            // Ignore
          }
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      
      if (!data.article) {
        throw new Error('Server returned empty article. Please try again.');
      }

      setArticle(data.article);
      setTopics(data.topics || []);
    } catch (err) {
      let errorMessage = 'Failed to generate article. Please try again.';
      
      if (err.name === 'AbortError' || err.message.includes('504') || err.message.includes('timeout')) {
        errorMessage = 'Request timeout. The first request can take 1-2 minutes as the AI model loads into memory. Please wait a moment and try again - subsequent requests will be faster. If this persists, check: docker-compose logs backend';
      } else if (err.message.includes('Failed to fetch') || err.message.includes('ERR_EMPTY_RESPONSE')) {
        errorMessage = 'Cannot connect to backend server. Please ensure:\n1. Backend is running: docker-compose ps\n2. Check backend logs: docker-compose logs backend\n3. Verify Ollama is running: docker exec ollama-mistral ollama list';
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      console.error('Error generating article:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setArticle(null);
    setTopics(null);
    setError(null);
  };

  return (
    <div className="home-page">
      <div className="home-header">
        <h1>AI Profile Assistant</h1>
        <p className="subtitle">
          Get personalized articles and discover topics tailored to your interests
        </p>
      </div>

      <div className="home-content">
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <div>
              <strong>Error:</strong> 
              <pre style={{ whiteSpace: 'pre-wrap', marginTop: '0.5rem' }}>{error}</pre>
              {(error.includes('Ollama') || error.includes('backend') || error.includes('Cannot connect')) && (
                <div className="error-hint">
                  <p><strong>Troubleshooting steps:</strong></p>
                  <ol style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
                    <li>Check if containers are running: <code>docker ps</code></li>
                    <li>Check backend logs: <code>docker-compose logs backend</code></li>
                    <li>Verify Ollama is running: <code>docker exec ollama-mistral ollama list</code></li>
                    <li>If Mistral model is missing, pull it: <code>docker exec ollama-mistral ollama pull mistral</code></li>
                    <li>Restart services: <code>docker-compose restart</code></li>
                  </ol>
                </div>
              )}
            </div>
          </div>
        )}

        {!article ? (
          <ProfileForm onSubmit={handleProfileSubmit} isLoading={isLoading} />
        ) : (
          <ArticleDisplay 
            article={article} 
            topics={topics} 
            onReset={handleReset}
          />
        )}

        {isLoading && (
          <div className="loading-overlay">
            <div className="loading-spinner"></div>
            <p>AI is analyzing your profile and generating your personalized article...</p>
            <p style={{ fontSize: '0.9rem', opacity: 0.8, marginTop: '0.5rem' }}>
              This may take 1-2 minutes on the first request while the model loads. Please be patient.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}