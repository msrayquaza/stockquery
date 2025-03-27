import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUsuarioInfo, logoutUser } from '../../api/auth';

// Si usas un archivo en /public/img, puedes referenciarlo con /img/logo.png
// Si prefieres guardarlo en /src/assets/img, importalo directamente:
import logoImage from '../../img/logo.png';
import defaultProfilePic from '../../img/default-profile.jpg'; 

const Navbar = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await getUsuarioInfo();
        setUser(data);
      } catch (error) {
        console.error('Usuario no autenticado', error);
      
      }
    };

    fetchUser();
  }, []);

  const handleLogout = async () => {
    try {
      await logoutUser();
   
      localStorage.removeItem('user');
      navigate('/login');
    } catch (error) {
      console.error('Error al cerrar sesión', error);
    }
  };


  const userName = user ? user.nombre : 'Invitado';
  
  const userProfilePic = user && user.imagen_perfil ? user.imagen_perfil : defaultProfilePic;


  const toggleSidebar = () => {
    const sidebarElement = document.getElementById('sidebar');
    if (sidebarElement) {
      sidebarElement.classList.toggle('collapsed');
    }
    const appElement = document.getElementById('app');
    if (appElement) {
      appElement.classList.toggle('expanded');
    }
  };

  return (
    <nav id="navbar">
      <div className="navbar-container">
        <div className="left-section">
          <button id="menu-toggle" className="menu-toggle" onClick={toggleSidebar}>
            ☰
          </button>
          <div className="logo-container">
            <img src={logoImage} alt="StockQuery Logo" className="logo-img" />
            <span className="logo">StockQuery</span>
          </div>
        </div>
        <div className="user-profile">
          <div className="profile-pic-container">
            <img
              src={userProfilePic}
              alt="Usuario"
              className="profile-pic"
              onError={(e) => {
              
                e.target.src = defaultProfilePic;
              }}
            />
          </div>
          <span className="user-text">{userName}</span>
          <button id="logoutBtn" className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
