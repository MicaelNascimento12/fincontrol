protegerPagina();

document.addEventListener("DOMContentLoaded", () => {
    carregarPerfil();
    carregarResumo();
    carregarGraficoCategorias();
    carregarFluxoMensal();

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

        atualizarUsuarioTopo(usuario.nome);
    } catch (erro) {
        console.error(erro);
    }
}


async function carregarResumo() {
    try {
        const resumo = await apiRequest("/dashboard/resumo");

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


async function carregarGraficoCategorias() {
    try {
        const dados = await apiRequest("/dashboard/gastos-por-categoria");

        const aviso = document.getElementById("semDadosCategorias");
        const canvas = document.getElementById("graficoCategorias");

        if (!dados.length) {
            aviso.style.display = "block";
            canvas.style.display = "none";
            return;
        }

        aviso.style.display = "none";
        canvas.style.display = "block";

        const labels = dados.map(item => item.categoria);
        const valores = dados.map(item => Number(item.total));

        const ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels,
                datasets: [
                    {
                        data: valores
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    } catch (erro) {
        console.error(erro);
    }
}


async function carregarFluxoMensal() {
    try {
        const dados = await apiRequest("/dashboard/fluxo-mensal");

        const aviso = document.getElementById("semDadosFluxo");
        const canvas = document.getElementById("graficoFluxoMensal");

        if (!dados.length) {
            aviso.style.display = "block";
            canvas.style.display = "none";
            return;
        }

        aviso.style.display = "none";
        canvas.style.display = "block";

        const labels = dados.map(item => item.mes);
        const receitas = dados.map(item => Number(item.receitas));
        const despesas = dados.map(item => Number(item.despesas));
        const saldo = dados.map(item => Number(item.saldo));

        const ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets: [
                    {
                        label: "Receitas",
                        data: receitas,
                        tension: 0.3
                    },
                    {
                        label: "Despesas",
                        data: despesas,
                        tension: 0.3
                    },
                    {
                        label: "Saldo",
                        data: saldo,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return formatarMoeda(value);
                            }
                        }
                    }
                }
            }
        });
    } catch (erro) {
        console.error(erro);
    }
}