"""
Script para popular o banco de dados com dados de exemplo.
Use apenas para testes e demonstrações.
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from database import db_manager
from services import AuthService, CategoriaService, LancamentoService, OrcamentoService
from models.lancamento import TipoLancamento


def popular_dados_exemplo():
    """Popula o banco com dados de exemplo dos últimos 6 meses."""
    
    print("🔄 Populando banco de dados com dados de exemplo...")
    
    # Inicializa o banco
    db_manager.init_database()
    
    # Cria usuário de exemplo
    print("\n👤 Criando usuário de exemplo...")
    sucesso, mensagem, usuario = AuthService.registrar_usuario(
        "Roberto Ricci",
        "ricci",
        "ricci123"
    )
    
    if not sucesso:
        print(f"❌ {mensagem}")
        return
    
    # print(f"✅ Usuário criado: {usuario.nome}")
    
    # # O sistema já cria categorias padrão, então vamos buscar algumas
    # print("\n🏷️ Obtendo categorias...")
    # categorias = CategoriaService.listar_categorias(usuario.id)
    
    # # Mapeia categorias por nome
    # cat_map = {cat['nome']: cat for cat in categorias}
    
    # # Define orçamentos para os últimos 3 meses
    # print("\n📋 Definindo orçamentos mensais...")
    
    # for i in range(3):
    #     data_ref = date.today() - relativedelta(months=i)
    #     mes = data_ref.month
    #     ano = data_ref.year
        
    #     print(f"\n   Orçamento de {mes:02d}/{ano}:")
        
    #     orcamentos = [
    #         ('Moradia', 1500.0),
    #         ('Alimentação', 800.0),
    #         ('Transporte', 400.0),
    #         ('Lazer', 300.0),
    #         ('Saúde', 200.0)
    #     ]
        
    #     for cat_nome, valor in orcamentos:
    #         if cat_nome in cat_map:
    #             sucesso, msg = OrcamentoService.definir_orcamento(
    #                 usuario.id,
    #                 cat_map[cat_nome]['id'],
    #                 mes,
    #                 ano,
    #                 valor
    #             )
    #             if sucesso:
    #                 print(f"      ✅ {cat_nome}: R$ {valor:.2f}")
    
    # # Cria lançamentos dos últimos 6 meses
    # print("\n💰 Criando lançamentos dos últimos 6 meses...")
    
    # for mes_offset in range(6):
    #     data_ref = date.today() - relativedelta(months=mes_offset)
    #     mes = data_ref.month
    #     ano = data_ref.year
        
    #     print(f"\n   Mês: {mes:02d}/{ano}")
        
    #     # Entradas do mês
    #     entradas = [
    #         ('Salário', 5000.0, f'Salário de {mes:02d}/{ano}', date(ano, mes, 5), TipoLancamento.FIXA),
    #         ('Investimentos', 150.0 + (mes_offset * 20), 'Rendimento CDB', date(ano, mes, 15), TipoLancamento.VARIAVEL),
    #     ]
        
    #     for cat_nome, valor, desc, data_lanc, tipo in entradas:
    #         if cat_nome in cat_map:
    #             sucesso, msg, _ = LancamentoService.criar_lancamento(
    #                 usuario.id,
    #                 cat_map[cat_nome]['id'],
    #                 data_lanc,
    #                 valor,
    #                 desc,
    #                 tipo
    #             )
    #             if sucesso:
    #                 print(f"      ✅ {desc}: R$ {valor:.2f}")
        
    #     # Despesas do mês (variação mensal)
    #     variacao = 1.0 + (mes_offset * 0.05)  # Pequena variação entre meses
        
    #     despesas = [
    #         ('Moradia', 1200.0, 'Aluguel', date(ano, mes, 10), TipoLancamento.FIXA),
    #         ('Moradia', 150.0 * variacao, 'Conta de luz', date(ano, mes, 15), TipoLancamento.VARIAVEL),
    #         ('Moradia', 80.0, 'Conta de água', date(ano, mes, 18), TipoLancamento.VARIAVEL),
    #         ('Alimentação', 450.0 * variacao, 'Supermercado', date(ano, mes, 12), TipoLancamento.VARIAVEL),
    #         ('Alimentação', 180.0 * variacao, 'Restaurantes', date(ano, mes, 20), TipoLancamento.VARIAVEL),
    #         ('Transporte', 250.0 * variacao, 'Combustível', date(ano, mes, 8), TipoLancamento.VARIAVEL),
    #         ('Transporte', 120.0, 'Uber/Taxi', date(ano, mes, 22), TipoLancamento.VARIAVEL),
    #         ('Lazer', 120.0 * variacao, 'Cinema e streaming', date(ano, mes, 14), TipoLancamento.VARIAVEL),
    #         ('Lazer', 80.0, 'Livros', date(ano, mes, 25), TipoLancamento.VARIAVEL),
    #         ('Saúde', 90.0 * variacao, 'Farmácia', date(ano, mes, 18), TipoLancamento.VARIAVEL),
    #         ('Educação', 200.0, 'Curso online', date(ano, mes, 5), TipoLancamento.FIXA),
    #     ]
        
    #     for cat_nome, valor, desc, data_lanc, tipo in despesas:
    #         if cat_nome in cat_map:
    #             sucesso, msg, _ = LancamentoService.criar_lancamento(
    #                 usuario.id,
    #                 cat_map[cat_nome]['id'],
    #                 data_lanc,
    #                 valor,
    #                 desc,
    #                 tipo
    #             )
    #             if sucesso:
    #                 print(f"      ✅ {desc}: R$ {valor:.2f}")
    
    # print("\n" + "=" * 60)
    # print("✅ Banco de dados populado com sucesso!")
    # print("\n📧 Credenciais de acesso:")
    # print("   Email: joao@email.com")
    # print("   Senha: senha123")
    # print("\n📊 Dados criados:")
    # print("   - 6 meses de lançamentos")
    # print("   - 3 meses de orçamentos")
    # print("   - Variação mensal nos valores")
    # print("=" * 60)


if __name__ == "__main__":
    try:
        popular_dados_exemplo()
    except Exception as e:
        print(f"\n❌ Erro ao popular banco: {str(e)}")
