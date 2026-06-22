CREATE DATABASE IF NOT EXISTS fincontrol
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fincontrol;

DROP TABLE IF EXISTS transacoes;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
  id            CHAR(36)      NOT NULL,
  nome          VARCHAR(100)  NOT NULL,
  email         VARCHAR(150)  NOT NULL,
  senha_hash    VARCHAR(255)  NOT NULL,
  data_criacao  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  CONSTRAINT UK_usuarios_email UNIQUE (email)
);

CREATE TABLE categorias (
  id       CHAR(36)      NOT NULL,
  user_id  CHAR(36)      NOT NULL,
  nome     VARCHAR(80)   NOT NULL,

  PRIMARY KEY (id),

  CONSTRAINT UK_categorias_usuario_nome UNIQUE (user_id, nome),

  CONSTRAINT FK_categorias_usuario
    FOREIGN KEY (user_id)
    REFERENCES usuarios (id)
    ON DELETE CASCADE
);

CREATE TABLE transacoes (
  id            CHAR(36)                          NOT NULL,
  user_id       CHAR(36)                          NOT NULL,
  categoria_id  CHAR(36)                          NOT NULL,
  tipo          ENUM('receita','despesa')          NOT NULL,
  status        ENUM('pendente','pago','cancelado') NOT NULL DEFAULT 'pago',
  valor         DECIMAL(10,2)                     NOT NULL,
  data          DATE                              NOT NULL,
  descricao     VARCHAR(255)                      NULL,
  observacao    TEXT                              NULL,

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