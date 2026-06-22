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

        document.getElementById("usuarioNome").textContent =
            usuario.nome;
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


async function carregarFluxoMensal() {
    try {
        const dados = await apiRequest("/dashboard/fluxo-mensal");

        const labels = dados.map(item => item.mes);
        const receitas = dados.map(item => Number(item.receitas));
        const despesas = dados.map(item => Number(item.despesas));
        const saldo = dados.map(item => Number(item.saldo));

        const ctx = document
            .getElementById("graficoFluxoMensal")
            .getContext("2d");

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
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                },
                scales: {
                    y: {
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