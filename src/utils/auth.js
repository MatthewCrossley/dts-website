export function setAuth(user) {
  window.localStorage.setItem("user", JSON.stringify(user));
}

export function getAuth() {
  return JSON.parse(window.localStorage.getItem("user"));
}

export function clearAuth() {
  window.localStorage.removeItem("user");
}
