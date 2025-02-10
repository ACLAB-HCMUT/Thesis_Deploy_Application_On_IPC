import React, { useState } from 'react';
import QRCodeComponent from '../../components/QRCodeComponent';

function About() {
  const [message, setMessage] = useState('');

  const handleClick = () => {
    setMessage('Xin chào từ trang About!');
  };

  return (
    <div>
      <h1>About</h1>
      <button onClick={handleClick}>Hello</button>
      {message && <p>{message}</p>}
      <QRCodeComponent />
    </div>
  );
}

export default About;


