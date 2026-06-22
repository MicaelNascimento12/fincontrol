const API_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("token");
}

function salvarToken(token) {
    localStorage.setItem("token", token);
}

function removerToken() {
    localStorage.removeItem("token");
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();

    const config = {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token && { Authorization: `Bearer ${token}` }),
            ...options.headers
        }
    };

    const response = await fetch(`${API_URL}${endpoint}`, config);

    if (!response.ok) {
        const erro = await response.json();
        throw new Error(erro.detail || "Erro na requisição");
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}