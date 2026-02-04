from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import datetime
from typing import List, Dict
from utils.formatador import FormatadorBR


class RelatorioFinanceiro:
    """Gerador de relatórios financeiros em PDF."""
    
    def __init__(self):
        self.formatador = FormatadorBR()
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        """Cria estilos personalizados para o relatório."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10
        ))
        
        # Texto alinhado à direita
        self.styles.add(ParagraphStyle(
            name='TextoDireita',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT
        ))
    
    def gerar_relatorio_mensal(
        self,
        usuario_nome: str,
        mes: int,
        ano: int,
        totais: Dict,
        lancamentos: List,
        orcamentos: List[Dict]
    ) -> BytesIO:
        """
        Gera relatório financeiro mensal em PDF.
        
        Args:
            usuario_nome: Nome do usuário
            mes: Mês do relatório
            ano: Ano do relatório
            totais: Dicionário com totais (entradas, despesas, saldo)
            lancamentos: Lista de lançamentos do mês
            orcamentos: Lista de orçamentos com comparações
            
        Returns:
            Buffer BytesIO com o PDF gerado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # Cabeçalho
        story.append(Paragraph(
            "Relatório Financeiro Mensal",
            self.styles['TituloPrincipal']
        ))
        
        story.append(Paragraph(
            f"{self.formatador.mes_ano_formatado(mes, ano)}",
            self.styles['Subtitulo']
        ))
        
        story.append(Paragraph(
            f"Usuário: {usuario_nome}",
            self.styles['Normal']
        ))
        
        story.append(Paragraph(
            f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 0.5*cm))
        
        # Resumo Financeiro
        story.append(Paragraph("Resumo Financeiro", self.styles['Subtitulo']))
        
        resumo_data = [
            ['Descrição', 'Valor'],
            ['Total de Entradas', self.formatador.formatar_moeda(totais['total_entradas'])],
            ['Total de Despesas', self.formatador.formatar_moeda(totais['total_despesas'])],
            ['Saldo do Mês', self.formatador.formatar_moeda(totais['saldo'])]
        ]
        
        resumo_table = Table(resumo_data, colWidths=[10*cm, 6*cm])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), 
             colors.HexColor('#27ae60') if totais['saldo'] >= 0 else colors.HexColor('#e74c3c'))
        ]))
        
        story.append(resumo_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Orçamento vs Realizado
        if orcamentos:
            story.append(Paragraph("Orçamento vs Realizado", self.styles['Subtitulo']))
            
            orc_data = [['Categoria', 'Planejado', 'Realizado', '% Utilizado']]
            
            for orc in orcamentos:
                orc_data.append([
                    orc['categoria_nome'],
                    self.formatador.formatar_moeda(orc['valor_planejado']),
                    self.formatador.formatar_moeda(orc['valor_realizado']),
                    self.formatador.formatar_percentual(orc['percentual_utilizado'])
                ])
            
            orc_table = Table(orc_data, colWidths=[6*cm, 3.5*cm, 3.5*cm, 3*cm])
            orc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(orc_table)
            story.append(Spacer(1, 0.5*cm))
        
        # Lançamentos Detalhados
        story.append(Paragraph("Lançamentos Detalhados", self.styles['Subtitulo']))
        
        # Separar por tipo de categoria
        entradas = [l for l in lancamentos if l['categoria_tipo'].value == 'Entrada']
        despesas = [l for l in lancamentos if l['categoria_tipo'].value == 'Despesa']
        
        # Entradas
        if entradas:
            story.append(Paragraph("Entradas", self.styles['Heading3']))
            
            entradas_data = [['Data', 'Categoria', 'Descrição', 'Valor']]
            
            for lanc in sorted(entradas, key=lambda x: x['data']):
                entradas_data.append([
                    self.formatador.formatar_data(lanc['data']),
                    lanc['categoria_nome'],
                    lanc['descricao'][:30] + '...' if len(lanc['descricao']) > 30 else lanc['descricao'],
                    self.formatador.formatar_moeda(lanc['valor'])
                ])
            
            entradas_table = Table(entradas_data, colWidths=[2.5*cm, 3.5*cm, 7*cm, 3*cm])
            entradas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(entradas_table)
            story.append(Spacer(1, 0.3*cm))
        
        # Despesas
        if despesas:
            story.append(Paragraph("Despesas", self.styles['Heading3']))
            
            despesas_data = [['Data', 'Categoria', 'Descrição', 'Valor']]
            
            for lanc in sorted(despesas, key=lambda x: x['data']):
                despesas_data.append([
                    self.formatador.formatar_data(lanc['data']),
                    lanc['categoria_nome'],
                    lanc['descricao'][:30] + '...' if len(lanc['descricao']) > 30 else lanc['descricao'],
                    self.formatador.formatar_moeda(lanc['valor'])
                ])
            
            despesas_table = Table(despesas_data, colWidths=[2.5*cm, 3.5*cm, 7*cm, 3*cm])
            despesas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(despesas_table)
        
        # Gera o PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
