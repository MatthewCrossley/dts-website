import { getAuth } from "../utils/auth";

export default function User({ user }) {
  const currentUser = getAuth();

  function handleDelete() {
    if (
      window.confirm(`Are you sure you want to delete user ${user.username}?`)
    ) {
      fetch(`http://localhost:8000/users/${user.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Basic ${btoa(
            `${currentUser.username}:${currentUser.password}`
          )}`,
        },
      })
        .then(async (response) => {
          if (response.ok) {
            window.location.reload();
          } else {
            document.getElementById(user.id).textContent =
              await response.text();
          }
        })
        .catch(
          (error) => (document.getElementById(user.id).textContent = error)
        );
    }
  }

  return (
    <>
      <div class="user">
        <h3>{user.username}</h3>
        <p>Admin: {user.admin ? "Yes" : "No"}</p>
        <button onClick={handleDelete}>Delete</button>
        <div className="error-message" id={`${user.id}`}></div>
      </div>
    </>
  );
}
