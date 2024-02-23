import React, { useContext, useRef, useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { useNavigate } from "react-router-dom";
import { SessionContext } from "../../context/session";
import { ConversationContext } from "../../context/conversations";

export default function NewDirectMessageModal({ isOpen, onClose }) {
  const navigate = useNavigate();
  const { session, setSession } = useContext(SessionContext);
  const { conversations, setConversations } = useContext(ConversationContext);
  const [users, setUsers] = useState([]);
  const [remainingUsers, setRemainingUsers] = useState([]);
  const [searchedUsers, setSearchedUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isOpen) {
      setInputValue("");
      setSearchedUsers([]);
      setError("");
    }
  }, [isOpen]);

  useEffect(() => {
    (async () => {
      const res = await fetch("/api/users");
      if (res.ok) {
        let allUsers = await res.json();
        allUsers = allUsers.filter((user) => user.id != session.id);
        setUsers(allUsers);
        setRemainingUsers(allUsers);
      } else {
        const errors = await res.json();
        console.log(errors);
      }
    })();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedUsers.length) {
      setError("Conversations must include at least one person.");
      return;
    }
    onClose();
    const res = await fetch("/api/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ users: [session, ...selectedUsers] }),
    });
    if (res.ok) {
      setSearchedUsers([]);
      setSelectedUsers([]);
      const conversation = await res.json();
      setRemainingUsers(users);
      if (!conversations.find((convo) => convo.id == conversation.id)) {
        setConversations((conversations) => [...conversations, conversation]);
        setSession((session) => {
          return {
            ...session,
            conversations: [...session.conversations, conversation],
          };
        });
      }
      navigate(`/conversations/${conversation.id}`);
    }
  };

  const handleChange = (e) => {
    setInputValue(e.target.value);
    if (e.target.value.length > 0) {
      const searchUsers = remainingUsers.filter((user) =>
        user.username.toLowerCase().startsWith(e.target.value.toLowerCase()),
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
    setRemainingUsers((remainingUsers) =>
      remainingUsers.filter((user) => user.username != username),
    );
    setSearchedUsers([]);
    setInputValue("");
  };

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="new-dm-modal">
      <div id="modal-background" onClick={onClose} />
      <div id="modal-content">
        <ul className="errors">
          <li>{error}</li>
        </ul>
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
    document.body,
  );
}
