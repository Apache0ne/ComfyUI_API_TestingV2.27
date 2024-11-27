import React from 'react';
import ModelSelector from './ModelSelector';
import '../styles/SideMenu.css'

const SideMenu = ({ isSideMenuOpen, toggleSideMenu, onModelSelect }) => {
  return (
    <div className={`side-menu ${isSideMenuOpen ? 'open' : ''}`}>
      <ModelSelector onModelSelect={onModelSelect} />
      <button className={`fold-button ${isSideMenuOpen ? 'open' : ''}`} onClick={toggleSideMenu}>
        {isSideMenuOpen ? '‹' : '›'}
      </button>
    </div>
  );
};

export default SideMenu;