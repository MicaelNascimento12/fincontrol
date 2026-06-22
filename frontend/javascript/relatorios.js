protegerPagina();

let categorias = [];
let transacoes = [];

document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("btnLogout").addEventListener("click", logout);
    document.getElementById("filtrosForm").addEventListener("submit", gerarRelatorio);
    document.getElementById("btnLimparFiltros").addEventListener("click", limparFiltros);

    await carregarPerfil();
    await carregarCategorias();
    await gerarRelatorio();
});


function formatarMoeda(valor) {
    return Number(valor).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );
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


async function carregarPerfil() {
    try {
        const usuario = await apiRequest("/usuarios/me");
        document.getElementById("usuarioNome").textContent = usuario.nome;
    } catch (erro) {
        console.error(erro);
    }
}


async function carregarCategorias() {
    categorias = await apiRequest("/categorias/");

    const filtroCategoria = document.getElementById("filtroCategoria");
    filtroCategoria.innerHTML = `<option value="">Todas</option>`;

    categorias.forEach(categoria => {
        filtroCategoria.innerHTML += `
            <option value="${categoria.id}">
                ${categoria.nome}
            </option>
        `;
    });
}


async function gerarRelatorio(event) {
    if (event) {
        event.preventDefault();
    }

    try {
        const tipo = document.getElementById("filtroTipo").value;
        const categoriaId = document.getElementById("filtroCategoria").value;
        const dataInicio = document.getElementById("dataInicio").value;
        const dataFim = document.getElementById("dataFim").value;

        if (dataInicio && dataFim && dataInicio > dataFim) {
            mostrarMensagem("A data inicial não pode ser maior que a data final.", "error");
            return;
        }

        const params = new URLSearchParams();

        if (tipo) {
            params.append("tipo", tipo);
        }

        if (categoriaId) {
            params.append("categoria_id", categoriaId);
        }

        if (dataInicio) {
            params.append("data_inicio", dataInicio);
        }

        if (dataFim) {
            params.append("data_fim", dataFim);
        }

        let endpoint = "/transacoes/";

        if ([...params].length > 0) {
            endpoint += `?${params.toString()}`;
        }

        transacoes = await apiRequest(endpoint);

        atualizarResumo();
        renderizarTabela();

    } catch (erro) {
        mostrarMensagem(erro.message, "error");
    }
}


function atualizarResumo() {
    let receitas = 0;
    let despesas = 0;

    transacoes.forEach(transacao => {
        if (transacao.status !== "pago") {
            return;
        }

        const valor = Number(transacao.valor);

        if (transacao.tipo === "receita") {
            receitas += valor;
        }

        if (transacao.tipo === "despesa") {
            despesas += valor;
        }
    });

    const saldo = receitas - despesas;

    document.getElementById("totalReceitas").textContent = formatarMoeda(receitas);
    document.getElementById("totalDespesas").textContent = formatarMoeda(despesas);
    document.getElementById("saldoPeriodo").textContent = formatarMoeda(saldo);
    document.getElementById("quantidadeRegistros").textContent =
        `${transacoes.length} registro${transacoes.length === 1 ? "" : "s"}`;
}


function renderizarTabela() {
    const tbody = document.getElementById("tabelaRelatorio");

    if (!transacoes.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6">Nenhuma transação encontrada.</td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = "";

    transacoes.forEach(transacao => {
        const categoria = categorias.find(cat => cat.id === transacao.categoria_id);

        tbody.innerHTML += `
            <tr>
                <td>${formatarData(transacao.data)}</td>
                <td>${transacao.descricao || "-"}</td>
                <td>${categoria ? categoria.nome : "-"}</td>
                <td>
                    <span class="badge ${transacao.tipo}">
                        ${transacao.tipo}
                    </span>
                </td>
                <td>
                    <span class="badge ${transacao.status}">
                        ${formatarStatus(transacao.status, transacao.tipo)}
                    </span>
                </td>
                <td>${formatarMoeda(transacao.valor)}</td>
            </tr>
        `;
    });
}


function limparFiltros() {
    document.getElementById("filtroTipo").value = "";
    document.getElementById("filtroCategoria").value = "";
    document.getElementById("dataInicio").value = "";
    document.getElementById("dataFim").value = "";

    gerarRelatorio();
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