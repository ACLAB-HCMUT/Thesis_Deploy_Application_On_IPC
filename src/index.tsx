import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux'; 
import App from './App.tsx';
import './index.css';
import { store, persistor } from './redux/store';
import { PersistGate } from 'redux-persist/integration/react';
const rootElement = document.getElementById('root');

// Kiểm tra nếu rootElement tồn tại trước khi tạo root
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <PersistGate persistor={persistor}>
      <Provider store={store}>  {/* Wrap App trong Provider */}
        <App />
      </Provider>
    </PersistGate>
  );
} else {
  console.error("Root element không tìm thấy");
}