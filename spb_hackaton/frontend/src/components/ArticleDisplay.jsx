import { useState } from 'react';
import './ArticleDisplay.css';

export default function ArticleDisplay({ article, topics, onReset }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(article);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Convert markdown links to clickable links
  const formatArticle = (text) => {
    // Replace markdown links [text](url) with HTML links
    const linkRegex = /\[([^\]]+)\]\(([^\)]+)\)/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = linkRegex.exec(text)) !== null) {
      // Add text before the link
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: text.substring(lastIndex, match.index)
        });
      }
      // Add the link
      parts.push({
        type: 'link',
        text: match[1],
        url: match[2]
      });
      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push({
        type: 'text',
        content: text.substring(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content: text }];
  };

  const formattedContent = formatArticle(article);

  return (
    <div className="article-display-container">
      <div className="article-header">
        <h2>Your Personalized Article</h2>
        <div className="article-actions">
          <button 
            onClick={handleCopy} 
            className="copy-button"
            title="Copy article"
          >
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
          <button 
            onClick={onReset} 
            className="reset-button"
            title="Create new article"
          >
            ✨ New Article
          </button>
        </div>
      </div>

      <div className="article-content">
        {formattedContent.map((part, index) => {
          if (part.type === 'link') {
            return (
              <a
                key={index}
                href={part.url}
                target="_blank"
                rel="noopener noreferrer"
                className="article-link"
              >
                {part.text}
              </a>
            );
          }
          return <span key={index}>{part.content}</span>;
        })}
      </div>

      {topics && topics.length > 0 && (
        <div className="topics-section">
          <h3>Topics of Interest</h3>
          <div className="topics-grid">
            {topics.map((topic, index) => (
              <a
                key={index}
                href={topic.url}
                target="_blank"
                rel="noopener noreferrer"
                className="topic-card"
              >
                <span className="topic-icon">🔗</span>
                <span className="topic-title">{topic.title}</span>
                <span className="topic-arrow">→</span>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

