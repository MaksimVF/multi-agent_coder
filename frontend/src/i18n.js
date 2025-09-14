


import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Translation files
import translationEN from './locales/en/translation.json';
import translationRU from './locales/ru/translation.json';
import translationES from './locales/es/translation.json';

// Initialize i18next
i18n
  .use(initReactI18next) // Passes i18n down to react-i18next
  .use(LanguageDetector) // Detects user language
  .init({
    resources: {
      en: {
        translation: translationEN
      },
      ru: {
        translation: translationRU
      },
      es: {
        translation: translationES
      }
    },
    fallbackLng: 'en', // Default language
    debug: true,
    interpolation: {
      escapeValue: false // React already safes from xss
    }
  });

export default i18n;


