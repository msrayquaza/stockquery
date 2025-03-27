import React from 'react';
import { NavLink } from 'react-router-dom'; 
// Asegúrate de instalar react-router-dom y configurar tus rutas

const Sidebar = () => {
  return (
    <aside id="sidebar">
      <h2 className="menu-title">Menú</h2>
      <ul className="sidebar-menu">
        <li className="menu-item">
          <NavLink to="/dashboard">
            <i className="fas fa-home icon"></i> 
            <span>Home</span>
          </NavLink>
        </li>
        <li className="menu-item">
          <NavLink to="/usuarios">
            <i className="fas fa-users icon"></i> 
            <span>Usuarios</span>
          </NavLink>
        </li>
        <li className="menu-item">
          <NavLink to="">
            <i className="fas fa-box icon"></i> 
            <span>VISTA</span>
          </NavLink>
        </li>
        <li className="menu-item">
          <NavLink to="">
            <i className="fas fa-search icon"></i> 
            <span>VISTA</span>
          </NavLink>
        </li>
        <li className="menu-item">
          <NavLink to="">
            <i className="fas fa-trash icon"></i> 
            <span>VISTA</span>
          </NavLink>
        </li>
        <li className="menu-item">
          <NavLink to="">
            <i className="fas fa-warehouse icon"></i> 
            <span>VISTA</span>
          </NavLink>
        </li>
        <li className="menu-item">
          <NavLink to="">
            <i className="fas fa-bell icon"></i> 
            <span>VISTA</span>
          </NavLink>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
