protegerPagina();

document.addEventListener("DOMContentLoaded", () => {

    carregarPerfil();
    carregarResumo();

    document
        .getElementById("btnLogout")
        .addEventListener("click", logout);

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


async function carregarPerfil() {

    try {

        const usuario = await apiRequest("/usuarios/me");

        document.getElementById("usuarioNome").textContent =
            usuario.nome;

    } catch (erro) {

        console.error(erro);

    }

}


async function carregarResumo() {

    try {

        const resumo =
            await apiRequest("/dashboard/resumo");

        document.getElementById("saldo").textContent =
            formatarMoeda(resumo.saldo);

        document.getElementById("receitas").textContent =
            formatarMoeda(resumo.receitas);

        document.getElementById("despesas").textContent =
            formatarMoeda(resumo.despesas);

    } catch (erro) {

        console.error(erro);

    }

}