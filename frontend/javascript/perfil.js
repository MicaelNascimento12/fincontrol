protegerPagina();

let usuarioLogado = null;

document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("btnLogout").addEventListener("click", logout);
    document.getElementById("perfilForm").addEventListener("submit", atualizarPerfil);
    document.getElementById("senhaForm").addEventListener("submit", alterarSenha);

    document.getElementById("btnEditarPerfil").addEventListener("click", habilitarEdicaoPerfil);
    document.getElementById("btnCancelarPerfil").addEventListener("click", cancelarEdicaoPerfil);

    document.getElementById("btnMostrarSenha").addEventListener("click", habilitarEdicaoSenha);
    document.getElementById("btnCancelarSenha").addEventListener("click", cancelarEdicaoSenha);

    bloquearPerfil();
    bloquearSenha();

    await carregarPerfil();
});


function bloquearPerfil() {
    document.getElementById("nome").disabled = true;
    document.getElementById("email").disabled = true;
    document.getElementById("dataCriacao").disabled = true;

    document.getElementById("btnEditarPerfil").style.display = "inline-block";
    document.getElementById("btnSalvarPerfil").style.display = "none";
    document.getElementById("btnCancelarPerfil").style.display = "none";
}


function habilitarEdicaoPerfil() {
    document.getElementById("nome").disabled = false;
    document.getElementById("email").disabled = false;

    document.getElementById("btnEditarPerfil").style.display = "none";
    document.getElementById("btnSalvarPerfil").style.display = "inline-block";
    document.getElementById("btnCancelarPerfil").style.display = "inline-block";
}


function cancelarEdicaoPerfil() {
    if (usuarioLogado) {
        document.getElementById("nome").value = usuarioLogado.nome;
        document.getElementById("email").value = usuarioLogado.email;
    }

    bloquearPerfil();
}


function bloquearSenha() {
    document.getElementById("senhaAtual").disabled = true;
    document.getElementById("novaSenha").disabled = true;
    document.getElementById("confirmarSenha").disabled = true;

    document.getElementById("btnMostrarSenha").style.display = "inline-block";
    document.getElementById("btnSalvarSenha").style.display = "none";
    document.getElementById("btnCancelarSenha").style.display = "none";
}


function habilitarEdicaoSenha() {
    document.getElementById("senhaAtual").disabled = false;
    document.getElementById("novaSenha").disabled = false;
    document.getElementById("confirmarSenha").disabled = false;

    document.getElementById("btnMostrarSenha").style.display = "none";
    document.getElementById("btnSalvarSenha").style.display = "inline-block";
    document.getElementById("btnCancelarSenha").style.display = "inline-block";
}


function cancelarEdicaoSenha() {
    document.getElementById("senhaForm").reset();
    bloquearSenha();
}


async function carregarPerfil() {
    try {
        usuarioLogado = await apiRequest("/usuarios/me");

        document.getElementById("usuarioNomeTopo").textContent = usuarioLogado.nome;
        document.getElementById("nome").value = usuarioLogado.nome;
        document.getElementById("email").value = usuarioLogado.email;

        document.getElementById("dataCriacao").value =
            new Date(usuarioLogado.data_criacao).toLocaleDateString("pt-BR");

    } catch (erro) {
        mostrarMensagem("mensagemPerfil", erro.message, "error");
    }
}


async function atualizarPerfil(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();

    try {
        const usuarioAtualizado = await apiRequest("/usuarios/me", {
            method: "PUT",
            body: JSON.stringify({ nome, email })
        });

        usuarioLogado = usuarioAtualizado;
        atualizarUsuarioTopo(usuarioLogado.nome);

        bloquearPerfil();
        mostrarMensagem("mensagemPerfil", "Perfil atualizado com sucesso!", "success");

    } catch (erro) {
        mostrarMensagem("mensagemPerfil", erro.message, "error");
    }
}


async function alterarSenha(event) {
    event.preventDefault();

    const senhaAtual = document.getElementById("senhaAtual").value;
    const novaSenha = document.getElementById("novaSenha").value;
    const confirmarSenha = document.getElementById("confirmarSenha").value;

    if (novaSenha !== confirmarSenha) {
        mostrarMensagem("mensagemSenha", "A confirmação da senha não confere.", "error");
        return;
    }

    try {
        await apiRequest("/usuarios/me/senha", {
            method: "PUT",
            body: JSON.stringify({
                senha_atual: senhaAtual,
                nova_senha: novaSenha
            })
        });

        document.getElementById("senhaForm").reset();

        bloquearSenha();
        mostrarMensagem("mensagemSenha", "Senha alterada com sucesso!", "success");

    } catch (erro) {
        mostrarMensagem("mensagemSenha", erro.message, "error");
    }
}


function mostrarMensagem(elementoId, texto, tipo) {
    const mensagem = document.getElementById(elementoId);

    mensagem.className = `message ${tipo}`;
    mensagem.textContent = texto;

    setTimeout(() => {
        mensagem.className = "message";
        mensagem.textContent = "";
    }, 3000);
}