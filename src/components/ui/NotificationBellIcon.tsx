import React, { useEffect, useState } from 'react';
import { Bell } from 'lucide-react';

interface NotificationBellIconProps {
  unreadCount?: number;
  size?: number;
  animated?: boolean;
}

const NotificationBellIcon: React.FC<NotificationBellIconProps> = ({
  unreadCount = 0,
  size = 24,
  animated = true
}) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [rotation, setRotation] = useState(0);
  const [prevCount, setPrevCount] = useState(unreadCount);

  // Simple animation effect using useState for rotation
  useEffect(() => {
    if (animated && unreadCount > prevCount) {
      setIsAnimating(true);
      
      // Create a simple bell shake effect with timed state changes
      let step = 0;
      const intervalId = setInterval(() => {
        switch (step) {
          case 0:
            setRotation(10);
            break;
          case 1:
            setRotation(-10);
            break;
          case 2:
            setRotation(10);
            break;
          case 3:
            setRotation(-10);
            break;
          case 4:
            setRotation(0);
            setIsAnimating(false);
            clearInterval(intervalId);
            break;
        }
        step++;
      }, 100);
      
      return () => {
        clearInterval(intervalId);
        setRotation(0);
      };
    }
    
    setPrevCount(unreadCount);
  }, [unreadCount, prevCount, animated]);

  return (
    <div className="relative">
      <div style={{ transform: `rotate(${rotation}deg)`, transition: 'transform 0.1s' }}>
        <Bell size={size} />
      </div>
      
      {unreadCount > 0 && (
        <span className="absolute -top-2 -right-2 flex h-5 w-5">
          {isAnimating && (
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
          )}
          <span className="relative inline-flex rounded-full h-5 w-5 bg-red-500 text-white text-xs font-bold items-center justify-center">
            {unreadCount <= 99 ? unreadCount : "99+"}
          </span>
        </span>
      )}
    </div>
  );
};

export default NotificationBellIcon;