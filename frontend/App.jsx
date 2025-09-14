import React from 'react';
import { useTranslation } from 'react-i18next';
import './i18n'; // Initialize i18n

function App() {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>{t('welcome')}</h1>
        <p>{t('description')}</p>

        <div className="language-selector">
          <button onClick={() => changeLanguage('en')}>English</button>
          <button onClick={() => changeLanguage('ru')}>Русский</button>
          <button onClick={() => changeLanguage('es')}>Español</button>
        </div>

        <nav>
          <ul>
            <li><a href="#dashboard">{t('dashboard')}</a></li>
            <li><a href="#projects">{t('projects')}</a></li>
            <li><a href="#agents">{t('agents')}</a></li>
            <li><a href="#tasks">{t('tasks')}</a></li>
          </ul>
        </nav>
      </header>
    </div>
  );
}

export default App;
