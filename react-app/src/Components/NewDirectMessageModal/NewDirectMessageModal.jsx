import React, { useContext, useRef, useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { useNavigate } from "react-router-dom";
import { SessionContext } from "../../context/session";

export default function NewDirectMessageModal({
  isOpen,
  onClose,
  setConversations,
}) {
  const navigate = useNavigate();
  const { session } = useContext(SessionContext);
  const [users, setUsers] = useState([]);
  const [searchedUsers, setSearchedUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    if (!isOpen) {
      setInputValue("");
      setSearchedUsers([]);
    }
  }, [isOpen]);

  useEffect(() => {
    (async () => {
      const res = await fetch("/api/users");
      if (res.ok) {
        let allUsers = await res.json();
        allUsers = allUsers.filter((user) => user.id != session.id);
        setUsers(allUsers);
      } else {
        const errors = await res.json();
        console.log(errors);
      }
    })();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    onClose();
    console.log({ users: [...selectedUsers, session] });
    const res = await fetch("/api/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ users: [session, ...selectedUsers] }),
    });
    if (res.ok) {
      const conversation = await res.json();
      setConversations((conversations) => [...conversations, conversation]);
      navigate(`/conversations/${conversation.id}`);
      setSelectedUsers([]);
    }
  };

  const handleChange = (e) => {
    setInputValue(e.target.value);
    if (e.target.value.length > 0) {
      const searchUsers = users.filter((user) =>
        user.username.toLowerCase().startsWith(e.target.value.toLowerCase())
      );
      setSearchedUsers(searchUsers);
    } else {
      setSearchedUsers([]);
    }
  };

  useEffect(() => {
    const dropdown = document.querySelector(".searched-recipients");
    if (!searchedUsers.length && dropdown) {
      dropdown.style.display = "none";
    } else if (searchedUsers.length && dropdown) {
      dropdown.style.display = "inline-block";
    }
  });

  const addUser = (e) => {
    const username = e.currentTarget.innerText;
    const chosenUser = searchedUsers.find((user) => user.username == username);
    setSelectedUsers((selectedUsers) => [...selectedUsers, chosenUser]);
    setUsers((users) => users.filter((user) => user.username != username));
    setSearchedUsers([]);
    setInputValue("");
  };

  useEffect(() => {
    console.log(selectedUsers);
  }, [selectedUsers]);

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
          <div className="selected-recipients">
            <span>Recipients: </span>
            {selectedUsers.map((user, idx) => (
              <span key={user.id}>
                {user.username}
                {idx + 1 < selectedUsers.length ? ", " : ""}
              </span>
            ))}
          </div>
          <div className="searched-recipients">
            <ul className="searched-recipients-list">
              {searchedUsers.map((user) => (
                <li
                  onClick={addUser}
                  className="searched-recipients-list-item"
                  key={user.id}
                >
                  {user.username}
                </li>
              ))}
            </ul>
          </div>
          <button>Create Conversation</button>
        </form>
      </div>
    </div>,
    document.body
  );
}
