import React from 'react';

const Header = () => {
  const scrollToSection = (id) => {
    const section = document.getElementById(id);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="bg-gray-900 text-white p-4 fixed w-full top-0 z-50">
      <nav className="flex justify-center space-x-8">
        <button onClick={() => scrollToSection('home')} className="hover:text-gray-400">
          Home
        </button>
        <button onClick={() => scrollToSection('benefits')} className="hover:text-gray-400">
          About
        </button>
        <button onClick={() => scrollToSection('services')} className="hover:text-gray-400">
          Services
        </button>
        <button onClick={() => scrollToSection('contact')} className="hover:text-gray-400">
          Contact
        </button>
      </nav>
    </header>
  );
};

export default Header;