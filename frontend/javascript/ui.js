const MENU_PRINCIPAL = [
    {
        pagina: "dashboard",
        texto: "Dashboard",
        href: "dashboard.html",
        icone: "layout-dashboard"
    },
    {
        pagina: "transacoes",
        texto: "Transações",
        href: "transacoes.html",
        icone: "arrow-left-right"
    },
    {
        pagina: "categorias",
        texto: "Categorias",
        href: "categorias.html",
        icone: "tags"
    },
    {
        pagina: "relatorios",
        texto: "Relatórios",
        href: "relatorios.html",
        icone: "file-text"
    },
    {
        pagina: "perfil",
        texto: "Perfil",
        href: "perfil.html",
        icone: "user"
    }
];


function renderizarLayout() {
    const paginaAtual = document.body.dataset.page;
    const tituloPagina = document.body.dataset.title || "FinControl";

    const sidebar = document.getElementById("appSidebar");
    const header = document.getElementById("appHeader");

    if (sidebar) {
        sidebar.innerHTML = `
            <div class="sidebar-brand">
                <div class="brand-mark">
                    <i data-lucide="chart-no-axes-column-increasing"></i>
                </div>

                <span class="brand-name">FinControl</span>
            </div>

            <nav class="sidebar-menu">
                ${MENU_PRINCIPAL.map(item => `
                    <a
                        href="${item.href}"
                        class="nav-link ${paginaAtual === item.pagina ? "active" : ""}"
                    >
                        <i data-lucide="${item.icone}" class="nav-icon"></i>
                        <span>${item.texto}</span>
                    </a>
                `).join("")}
            </nav>

            <button id="btnLogout" class="btn-logout" type="button">
                <i data-lucide="log-out"></i>
                <span>Sair</span>
            </button>
        `;
    }

    if (header) {
        header.innerHTML = `
            <h1>${tituloPagina}</h1>

            <div class="topbar-actions">
                <span class="notification-icon" aria-label="Notificações">
                    <i data-lucide="bell"></i>
                </span>

                <a href="perfil.html" class="user-summary">
                    <span class="user-avatar" id="usuarioAvatar">
                        FC
                    </span>

                    <span class="user-summary-name" id="usuarioNome">
                        Carregando...
                    </span>

                    <i data-lucide="chevron-down" class="user-chevron"></i>
                </a>
            </div>
        `;
    }

    renderizarIcones();
}


function obterIniciais(nome) {
    if (!nome) {
        return "FC";
    }

    const partes = nome
        .trim()
        .split(/\s+/)
        .filter(Boolean);

    if (partes.length === 1) {
        return partes[0].substring(0, 2).toUpperCase();
    }

    return (
        partes[0][0] +
        partes[partes.length - 1][0]
    ).toUpperCase();
}


function atualizarUsuarioTopo(nome) {
    const nomeElemento = document.getElementById("usuarioNome");
    const avatarElemento = document.getElementById("usuarioAvatar");

    if (nomeElemento) {
        nomeElemento.textContent = nome;
    }

    if (avatarElemento) {
        avatarElemento.textContent = obterIniciais(nome);
    }
}


function renderizarIcones() {
    if (!window.lucide) {
        return;
    }

    window.lucide.createIcons({
        attrs: {
            "stroke-width": 1.9
        }
    });
}


document.addEventListener("DOMContentLoaded", renderizarLayout);