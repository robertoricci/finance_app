from typing import Any
import locale


class FormatadorBR:
    """Formatador de valores para padrão brasileiro."""
    
    @staticmethod
    def formatar_moeda(valor: float) -> str:
        """
        Formata valor numérico como moeda brasileira.
        
        Args:
            valor: Valor numérico
            
        Returns:
            String formatada (ex: 'R$ 1.234,56')
        """
        try:
            return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        except:
            return "R$ 0,00"
    
    @staticmethod
    def formatar_percentual(valor: float, casas_decimais: int = 1) -> str:
        """
        Formata valor como percentual.
        
        Args:
            valor: Valor numérico
            casas_decimais: Número de casas decimais
            
        Returns:
            String formatada (ex: '75,5%')
        """
        try:
            return f"{valor:.{casas_decimais}f}%".replace('.', ',')
        except:
            return "0,0%"
    
    @staticmethod
    def formatar_data(data: Any) -> str:
        """
        Formata data no padrão brasileiro.
        
        Args:
            data: Objeto date ou datetime
            
        Returns:
            String formatada (ex: '15/01/2024')
        """
        try:
            return data.strftime('%d/%m/%Y')
        except:
            return ""
    
    @staticmethod
    def mes_ano_formatado(mes: int, ano: int) -> str:
        """
        Formata mês e ano por extenso.
        
        Args:
            mes: Número do mês (1-12)
            ano: Ano
            
        Returns:
            String formatada (ex: 'Janeiro de 2024')
        """
        meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        
        try:
            return f"{meses[mes - 1]} de {ano}"
        except:
            return f"{mes}/{ano}"
