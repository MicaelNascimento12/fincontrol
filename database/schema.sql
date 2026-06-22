-- ============================================================
-- FinControl – Schema do Banco de Dados
-- Versão: 1.0
-- Autor: Micael Nascimento
-- ============================================================

CREATE DATABASE IF NOT EXISTS fincontrol
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fincontrol;

-- ============================================================
-- TABELA: usuarios
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
  id            INT           NOT NULL AUTO_INCREMENT,
  nome          VARCHAR(100)  NOT NULL,
  email         VARCHAR(150)  NOT NULL,
  senha_hash    VARCHAR(255)  NOT NULL,
  data_criacao  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  CONSTRAINT UK_usuarios_email UNIQUE (email)
);

-- ============================================================
-- TABELA: categorias
-- ============================================================
CREATE TABLE IF NOT EXISTS categorias (
  id       INT          NOT NULL AUTO_INCREMENT,
  user_id  INT          NOT NULL,
  nome     VARCHAR(80)  NOT NULL,

  PRIMARY KEY (id),
  CONSTRAINT FK_categorias_usuario
    FOREIGN KEY (user_id)
    REFERENCES usuarios (id)
    ON DELETE CASCADE
);

-- ============================================================
-- TABELA: transacoes
-- ============================================================
CREATE TABLE IF NOT EXISTS transacoes (
  id            INT                        NOT NULL AUTO_INCREMENT,
  user_id       INT                        NOT NULL,
  categoria_id  INT                        NOT NULL,
  tipo          ENUM('receita','despesa')  NOT NULL,
  valor         DECIMAL(10,2)              NOT NULL,
  data          DATE                       NOT NULL,
  descricao     VARCHAR(255)               NULL,

  PRIMARY KEY (id),
  CONSTRAINT FK_transacoes_usuario
    FOREIGN KEY (user_id)
    REFERENCES usuarios (id)
    ON DELETE CASCADE,
  CONSTRAINT FK_transacoes_categoria
    FOREIGN KEY (categoria_id)
    REFERENCES categorias (id)
    ON DELETE RESTRICT,
  CONSTRAINT CHK_transacoes_valor
    CHECK (valor > 0)
);