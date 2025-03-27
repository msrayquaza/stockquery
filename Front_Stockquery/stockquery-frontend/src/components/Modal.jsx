// src/components/Modal.jsx
import React from 'react';
import '../styles/Modal.css';

const Modal = ({ title, children, onClose }) => {
  const handleBackdropClick = () => {
    if (onClose) onClose();
  };

  const stopPropagation = (e) => {
    e.stopPropagation();
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content" onClick={stopPropagation}>
        <div className="modal-header">
          <h2 className="modal-title">{title}</h2>
          <button className="close-button" onClick={onClose}>
            &times;
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
