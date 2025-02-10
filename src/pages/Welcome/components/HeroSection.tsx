import React from 'react';

function HeroSection() {
  return (
    <div className="background-welcome flex items-center justify-center text-white h-screen">
      <div className="text-center">
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-medium mb-4">
            Welcome to our site!
          </h1>
        <button className="mt-4 px-8 sm:px-6 sm:py-3 md:px-8 md:py-4 py-4 bg-white bg-opacity-40 text-white rounded-full font-medium hover:bg-gray-200 hover:text-black transition-all duration-500">
        {/* <button className="mt-4 px-4 py-2 sm:px-6 sm:py-3 md:px-8 md:py-4 text-sm sm:text-lg md:text-xl lg:text-2xl bg-white bg-opacity-40 text-white rounded-full font-semibold hover:bg-gray-200 transition duration-500"> */}
          Read More
        </button>
      </div>
    </div>

  );
};

export default HeroSection;
