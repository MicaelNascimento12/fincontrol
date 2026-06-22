-- ============================================================
-- FinControl – Views
-- Versão: 1.0
-- Autor: Micael Nascimento
-- ============================================================

USE fincontrol;

-- ============================================================
-- VIEW: vw_saldo_usuario
-- Retorna o saldo atual de cada usuário
-- Saldo = total de receitas - total de despesas (RN-06)
-- ============================================================
CREATE OR REPLACE VIEW vw_saldo_usuario AS
SELECT
  u.id                                            AS user_id,
  u.nome                                          AS nome_usuario,
  COALESCE(SUM(CASE WHEN t.tipo = 'receita'
    THEN t.valor ELSE 0 END), 0)                  AS total_receitas,
  COALESCE(SUM(CASE WHEN t.tipo = 'despesa'
    THEN t.valor ELSE 0 END), 0)                  AS total_despesas,
  COALESCE(SUM(CASE WHEN t.tipo = 'receita'
    THEN t.valor ELSE -t.valor END), 0)           AS saldo_atual
FROM usuarios u
LEFT JOIN transacoes t ON t.user_id = u.id
GROUP BY u.id, u.nome;

-- ============================================================
-- VIEW: vw_transacoes_completas
-- Retorna transações com nome da categoria incluído
-- Evita JOIN repetido no back-end
-- ============================================================
CREATE OR REPLACE VIEW vw_transacoes_completas AS
SELECT
  t.id             AS transacao_id,
  t.user_id,
  t.tipo,
  t.valor,
  t.data,
  t.descricao,
  c.id             AS categoria_id,
  c.nome           AS categoria_nome
FROM transacoes t
INNER JOIN categorias c ON c.id = t.categoria_id;

-- ============================================================
-- VIEW: vw_gastos_por_categoria
-- Retorna total gasto por categoria de cada usuário
-- Usada no gráfico de despesas por categoria (RF-23)
-- ============================================================
CREATE OR REPLACE VIEW vw_gastos_por_categoria AS
SELECT
  t.user_id,
  c.id             AS categoria_id,
  c.nome           AS categoria_nome,
  COALESCE(SUM(t.valor), 0) AS total_gasto
FROM transacoes t
INNER JOIN categorias c ON c.id = t.categoria_id
WHERE t.tipo = 'despesa'
GROUP BY t.user_id, c.id, c.nome;