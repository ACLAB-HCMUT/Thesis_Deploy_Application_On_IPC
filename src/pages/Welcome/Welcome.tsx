import React from 'react';
import Navbar from './components/navbar.tsx';
import HeroSection from './components/HeroSection.tsx';


function Welcome() {
  
  return (
    <div className='welcome'>
      <Navbar />
      <HeroSection />
    </div>
  );
}

export default Welcome;


