import React, { useState } from 'react';

export function SwitchToggle() {
    const [enabled, setEnabled] = useState(false);
    return (
      <div 
        className={`flex items-center space-x-2 p-2 rounded-full transition-colors cursor-pointer`} 
        onClick={() => setEnabled(!enabled)}
      >
        
        <div 
          className={`w-20 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out shadow-md ${enabled ? 'bg-green-400' : 'bg-gray-400'}`}
        >
          <div 
            className={`w-8 h-8 rounded-full transition-transform transform ${enabled ? 'bg-green-700 translate-x-9' : 'bg-gray-600 translate-x-0'}`}
          />
        </div>
        <span className={`font-medium ${enabled ? 'text-green-600' : 'text-gray-500'}`}>{enabled ? 'ON' : 'OFF'}</span>
      </div>
    );
  }
  