const BASE_URL = "http://127.0.0.1:8000"; // Your Django URL

export const authenticatedFetch = async (endpoint, options = {}) => {
  const token = localStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Optional: Handle expired token here (e.g., redirect to login)
    console.warn("Token expired or invalid");
  }

  return response;
};