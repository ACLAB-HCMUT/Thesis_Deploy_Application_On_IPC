import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux'; 
import App from './App.tsx';
import './index.css';
import { store } from './redux/store';
const rootElement = document.getElementById('root');

// Kiểm tra nếu rootElement tồn tại trước khi tạo root
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <Provider store={store}>  {/* Wrap App trong Provider */}
      <App />
    </Provider>
  );
} else {
  console.error("Root element không tìm thấy");
}