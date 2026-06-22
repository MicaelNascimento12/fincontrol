protegerPagina();

let categorias = [];
let transacoes = [];
let transacaoIdParaExcluir = null;

document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("btnLogout").addEventListener("click", logout);
    document.getElementById("transacaoForm").addEventListener("submit", salvarTransacao);
    document.getElementById("btnCancelarEdicao").addEventListener("click", limparFormulario);
    document.getElementById("filtroTipo").addEventListener("change", listarTransacoes);
    document.getElementById("filtroCategoria").addEventListener("change", listarTransacoes);
    document.getElementById("tipo").addEventListener("change", atualizarOpcoesStatus);

    document.getElementById("btnFecharModalTransacao")
        .addEventListener("click", fecharModalExcluirTransacao);

    document.getElementById("btnConfirmarExcluirTransacao")
        .addEventListener("click", confirmarExclusaoTransacao);

    preencherDataAtual();
    atualizarOpcoesStatus();
    esconderCancelarEdicao();

    await carregarPerfil();
    await carregarCategorias();
    await listarTransacoes();
});


function formatarMoeda(valor) {
    return Number(valor).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}


function formatarData(data) {
    return new Date(data + "T00:00:00").toLocaleDateString("pt-BR");
}


function formatarStatus(status, tipo) {
    if (tipo === "receita") {
        if (status === "pago") return "recebido";
        if (status === "pendente") return "a receber";
        return "cancelado";
    }

    return status;
}


function atualizarOpcoesStatus() {
    const tipo = document.getElementById("tipo").value;
    const status = document.getElementById("status");

    if (tipo === "receita") {
        status.innerHTML = `
            <option value="pago">Recebido</option>
            <option value="pendente">A receber</option>
            <option value="cancelado">Cancelado</option>
        `;
    } else {
        status.innerHTML = `
            <option value="pago">Pago</option>
            <option value="pendente">Pendente</option>
            <option value="cancelado">Cancelado</option>
        `;
    }
}


function mostrarCancelarEdicao() {
    document.getElementById("btnCancelarEdicao").style.display = "inline-block";
}


function esconderCancelarEdicao() {
    document.getElementById("btnCancelarEdicao").style.display = "none";
}


async function carregarPerfil() {
    try {
        const usuario = await apiRequest("/usuarios/me");
        atualizarUsuarioTopo(usuario.nome);
    } catch (erro) {
        console.error(erro);
    }
}


async function carregarCategorias() {
    categorias = await apiRequest("/categorias/");

    const selectCategoria = document.getElementById("categoria");
    const filtroCategoria = document.getElementById("filtroCategoria");

    selectCategoria.innerHTML = "";
    filtroCategoria.innerHTML = `<option value="">Todas as categorias</option>`;

    categorias.forEach(categoria => {
        selectCategoria.innerHTML += `
            <option value="${categoria.id}">
                ${categoria.nome}
            </option>
        `;

        filtroCategoria.innerHTML += `
            <option value="${categoria.id}">
                ${categoria.nome}
            </option>
        `;
    });
}


async function listarTransacoes() {
    try {
        const tipo = document.getElementById("filtroTipo").value;
        const categoriaId = document.getElementById("filtroCategoria").value;

        let endpoint = "/transacoes/";
        const params = new URLSearchParams();

        if (tipo) params.append("tipo", tipo);
        if (categoriaId) params.append("categoria_id", categoriaId);

        if ([...params].length > 0) {
            endpoint += `?${params.toString()}`;
        }

        transacoes = await apiRequest(endpoint);
        renderizarTabela();
    } catch (erro) {
        console.error(erro);
    }
}


function renderizarTabela() {
    const tbody = document.getElementById("tabelaTransacoes");

    if (!transacoes.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7">Nenhuma transação encontrada.</td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = "";

    transacoes.forEach(transacao => {
        const categoria = categorias.find(
            item => item.id === transacao.categoria_id
        );

        const iconeTipo =
            transacao.tipo === "receita"
                ? "arrow-up"
                : "arrow-down";

        tbody.innerHTML += `
            <tr>
                <td>${formatarData(transacao.data)}</td>

                <td>${transacao.descricao || "-"}</td>

                <td>${categoria ? categoria.nome : "-"}</td>

                <td>
                    <span class="badge ${transacao.tipo}">
                        <i data-lucide="${iconeTipo}"></i>
                        ${transacao.tipo}
                    </span>
                </td>

                <td>
                    <span class="badge ${transacao.status}">
                        <i data-lucide="circle-check"></i>
                        ${formatarStatus(
                            transacao.status,
                            transacao.tipo
                        )}
                    </span>
                </td>

                <td>${formatarMoeda(transacao.valor)}</td>

                <td>
                    <button
                        class="btn-small btn-edit"
                        onclick="editarTransacao('${transacao.id}')"
                    >
                        <i data-lucide="pencil"></i>
                        Editar
                    </button>

                    <button
                        class="btn-small btn-delete"
                        onclick="abrirModalExcluirTransacao('${transacao.id}')"
                    >
                        <i data-lucide="trash-2"></i>
                        Excluir
                    </button>
                </td>
            </tr>
        `;
    });

    renderizarIcones();
}


async function salvarTransacao(event) {
    event.preventDefault();

    const id = document.getElementById("transacaoId").value;

    const dados = {
        categoria_id: document.getElementById("categoria").value,
        tipo: document.getElementById("tipo").value,
        status: document.getElementById("status").value,
        valor: Number(document.getElementById("valor").value),
        data: document.getElementById("data").value,
        descricao: document.getElementById("descricao").value || null,
        observacao: document.getElementById("observacao").value || null
    };

    try {
        if (id) {
            await apiRequest(`/transacoes/${id}`, {
                method: "PUT",
                body: JSON.stringify(dados)
            });

            mostrarMensagem("Transação atualizada com sucesso!", "success");
        } else {
            await apiRequest("/transacoes/", {
                method: "POST",
                body: JSON.stringify(dados)
            });

            mostrarMensagem("Transação cadastrada com sucesso!", "success");
        }

        limparFormulario();
        await listarTransacoes();

    } catch (erro) {
        mostrarMensagem(erro.message, "error");
    }
}


function editarTransacao(id) {
    const transacao = transacoes.find(item => item.id === id);

    if (!transacao) return;

    document.getElementById("formTitulo").textContent = "Editar Transação";
    document.getElementById("transacaoId").value = transacao.id;
    document.getElementById("descricao").value = transacao.descricao || "";
    document.getElementById("valor").value = transacao.valor;
    document.getElementById("data").value = transacao.data;
    document.getElementById("tipo").value = transacao.tipo;
    atualizarOpcoesStatus();
    document.getElementById("status").value = transacao.status;
    document.getElementById("categoria").value = transacao.categoria_id;
    document.getElementById("observacao").value = transacao.observacao || "";
    document.getElementById("btnSalvar").innerHTML = `
    <i data-lucide="save"></i>
    <span>Salvar alterações</span>
`;

renderizarIcones();
    
    mostrarCancelarEdicao();
    window.scrollTo({ top: 0, behavior: "smooth" });
}


function limparFormulario() {
    document.getElementById("formTitulo").textContent = "Nova Transação";
    document.getElementById("transacaoId").value = "";
    document.getElementById("descricao").value = "";
    document.getElementById("valor").value = "";
    document.getElementById("observacao").value = "";
    document.getElementById("tipo").value = "receita";
    document.getElementById("btnSalvar").innerHTML = `
    <i data-lucide="save"></i>
    <span>Salvar</span>
`;

renderizarIcones();

    atualizarOpcoesStatus();
    document.getElementById("status").value = "pago";

    if (categorias.length) {
        document.getElementById("categoria").value = categorias[0].id;
    }

    preencherDataAtual();
    esconderCancelarEdicao();
}


function preencherDataAtual() {
    const hoje = new Date().toISOString().split("T")[0];
    document.getElementById("data").value = hoje;
}


function abrirModalExcluirTransacao(id) {
    transacaoIdParaExcluir = id;
    document.getElementById("modalExcluirTransacao").classList.add("active");
}


function fecharModalExcluirTransacao() {
    transacaoIdParaExcluir = null;
    document.getElementById("modalExcluirTransacao").classList.remove("active");
}


async function confirmarExclusaoTransacao() {
    if (!transacaoIdParaExcluir) return;

    try {
        await apiRequest(`/transacoes/${transacaoIdParaExcluir}`, {
            method: "DELETE"
        });

        fecharModalExcluirTransacao();
        mostrarMensagem("Transação excluída com sucesso!", "success");
        await listarTransacoes();

    } catch (erro) {
        fecharModalExcluirTransacao();
        mostrarMensagem(erro.message, "error");
    }
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