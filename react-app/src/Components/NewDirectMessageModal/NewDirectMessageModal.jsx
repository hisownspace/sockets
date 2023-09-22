import React, { useContext, useRef, useState, useEffect } from "react";
import ReactDOM from "react-dom";

export default function NewDirectMessageModal({ isOpen, onClose }) {
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    if (!isOpen) {
      setInputValue("");
    }
  }, [isOpen]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onClose();
  };

  const handleChange = (e) => {
    setInputValue(e.target.value);
    if (e.target.value.length > 1) {
      (async () => {
        const res = await fetch("/api/users/search?user=" + e.target.value);
        if (res.ok) {
          const users = await res.json();
          console.log(users);
        }
      })();
    }
  };

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="new-dm-modal">
      <div id="modal-background" onClick={onClose} />
      <div id="modal-content">
        <form className="new-dm-form" onSubmit={handleSubmit}>
          <input
            className="new-dm-button"
            value={inputValue}
            onChange={handleChange}
          />
          <button>Create Conversation</button>
          <div className="selected-recipients"></div>
        </form>
      </div>
    </div>,
    document.body
  );
}
