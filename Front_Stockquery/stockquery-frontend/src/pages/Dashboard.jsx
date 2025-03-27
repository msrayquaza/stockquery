
import React from 'react';
import Navbar from '../components/navigation/Navbar';
import Sidebar from '../components/navigation/Sidebar';

const Dashboard = () => {
  return (
    <div className="container">
      <Navbar />
      <Sidebar />
      <div id="app">
        <h2>¡Bienvenido al Dashboard!</h2>
        <p>Contenido principal...</p>
      </div>
    </div>
  );
};

export default Dashboard;
