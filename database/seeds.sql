-- ============================================================
-- FinControl – Seeds
-- Versão: 1.0
-- Autor: Micael Nascimento
-- ============================================================

USE fincontrol;

-- ============================================================
-- CATEGORIAS PADRÃO
-- Estas categorias não são inseridas diretamente no banco.
-- Elas são copiadas para cada novo usuário no momento do
-- cadastro, via back-end (RF-16, RN-08).
--
-- Categorias padrão do sistema:
-- 1. Alimentação
-- 2. Transporte
-- 3. Saúde
-- 4. Educação
-- 5. Moradia
-- 6. Lazer
-- 7. Investimentos
-- ============================================================

-- ============================================================
-- USUÁRIO DE TESTE (apenas para ambiente de desenvolvimento)
-- NUNCA executar em produção
-- ============================================================

INSERT INTO usuarios (nome, email, senha_hash) VALUES
(
  'Micael Teste',
  'micael@teste.com',
  '$2b$12$placeholder_substituir_por_hash_real'
);

-- Categorias do usuário de teste (id = 1)
INSERT INTO categorias (user_id, nome) VALUES
(1, 'Alimentação'),
(1, 'Transporte'),
(1, 'Saúde'),
(1, 'Educação'),
(1, 'Moradia'),
(1, 'Lazer'),
(1, 'Investimentos');