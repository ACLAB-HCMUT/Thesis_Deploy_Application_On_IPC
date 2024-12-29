import React from 'react';
import { QRCodeCanvas } from 'qrcode.react';

function QRCodeComponent() {
  const ipAddress = window.location.href;

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Scan the QR code to connect</h2>
      <QRCodeCanvas value={ipAddress} size={150} />
    </div>
  );
}

export default QRCodeComponent;
