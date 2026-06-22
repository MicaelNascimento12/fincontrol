protegerPagina();

let categorias = [];

document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("btnLogout").addEventListener("click", logout);
    document.getElementById("categoriaForm").addEventListener("submit", salvarCategoria);
    document.getElementById("btnCancelarEdicao").addEventListener("click", limparFormulario);

    await carregarPerfil();
    await listarCategorias();
});


async function carregarPerfil() {
    try {
        const usuario = await apiRequest("/usuarios/me");
        document.getElementById("usuarioNome").textContent = usuario.nome;
    } catch (erro) {
        console.error(erro);
    }
}


async function listarCategorias() {
    try {
        categorias = await apiRequest("/categorias/");
        renderizarTabela();
    } catch (erro) {
        console.error(erro);
    }
}


function renderizarTabela() {
    const tbody = document.getElementById("tabelaCategorias");

    if (!categorias.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="2">Nenhuma categoria encontrada.</td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = "";

    categorias.forEach(categoria => {
        tbody.innerHTML += `
            <tr>
                <td>${categoria.nome}</td>
                <td>
                    <button class="btn-small btn-edit" onclick="editarCategoria('${categoria.id}')">
                        Editar
                    </button>

                    <button class="btn-small btn-delete" onclick="excluirCategoria('${categoria.id}')">
                        Excluir
                    </button>
                </td>
            </tr>
        `;
    });
}


async function salvarCategoria(event) {
    event.preventDefault();

    const id = document.getElementById("categoriaId").value;
    const nome = document.getElementById("nome").value.trim();

    if (!nome) {
        mostrarMensagem("Informe o nome da categoria.", "error");
        return;
    }

    const dados = { nome };

    try {
        if (id) {
            await apiRequest(`/categorias/${id}`, {
                method: "PUT",
                body: JSON.stringify(dados)
            });

            mostrarMensagem("Categoria atualizada com sucesso!", "success");
        } else {
            await apiRequest("/categorias/", {
                method: "POST",
                body: JSON.stringify(dados)
            });

            mostrarMensagem("Categoria cadastrada com sucesso!", "success");
        }

        limparFormulario();
        await listarCategorias();

    } catch (erro) {
        mostrarMensagem(erro.message, "error");
    }
}


function editarCategoria(id) {
    const categoria = categorias.find(item => item.id === id);

    if (!categoria) {
        return;
    }

    document.getElementById("formTitulo").textContent = "Editar Categoria";
    document.getElementById("categoriaId").value = categoria.id;
    document.getElementById("nome").value = categoria.nome;

    window.scrollTo({ top: 0, behavior: "smooth" });
}


async function excluirCategoria(id) {
    const confirmar = confirm(
        "Tem certeza que deseja excluir esta categoria? Categorias com transações vinculadas não poderão ser excluídas."
    );

    if (!confirmar) {
        return;
    }

    try {
        await apiRequest(`/categorias/${id}`, {
            method: "DELETE"
        });

        mostrarMensagem("Categoria excluída com sucesso!", "success");
        await listarCategorias();

    } catch (erro) {
        mostrarMensagem(erro.message, "error");
    }
}


function limparFormulario() {
    document.getElementById("formTitulo").textContent = "Nova Categoria";
    document.getElementById("categoriaId").value = "";
    document.getElementById("nome").value = "";
}


function mostrarMensagem(texto, tipo) {
    const mensagem = document.getElementById("mensagem");

    mensagem.className = `message ${tipo}`;
    mensagem.textContent = texto;

    setTimeout(() => {
        mensagem.className = "message";
        mensagem.textContent = "";
    }, 3000);
}