async function login(email, senha) {
    const resposta = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({
            email,
            senha
        })
    });

    salvarToken(resposta.access_token);
    window.location.href = "dashboard.html";
}

async function cadastrar(nome, email, senha) {
    const resposta = await apiRequest("/auth/cadastro", {
        method: "POST",
        body: JSON.stringify({
            nome,
            email,
            senha
        })
    });

    salvarToken(resposta.access_token);
    window.location.href = "dashboard.html";
}

function logout() {
    removerToken();
    window.location.href = "login.html";
}

function protegerPagina() {
    const token = getToken();

    if (!token) {
        window.location.href = "login.html";
    }
}

function redirecionarSeLogado() {
    const token = getToken();

    if (token) {
        window.location.href = "dashboard.html";
    }
}