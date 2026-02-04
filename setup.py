#!/usr/bin/env python3
"""
Script de inicialização do Sistema de Finanças Pessoais.
Instala dependências e inicia a aplicação.
"""

import subprocess
import sys
import os


def verificar_python():
    """Verifica a versão do Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")


def instalar_dependencias():
    """Instala as dependências do projeto."""
    print("\n📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências!")
        sys.exit(1)


def iniciar_aplicacao():
    """Inicia a aplicação Streamlit."""
    print("\n🚀 Iniciando aplicação...")
    print("   A aplicação será aberta no navegador automaticamente.")
    print("   Use Ctrl+C para encerrar.")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Aplicação encerrada.")


def main():
    """Função principal."""
    print("=" * 60)
    print("💰 Sistema de Finanças Pessoais")
    print("=" * 60)
    
    verificar_python()
    
    if not os.path.exists("requirements.txt"):
        print("❌ Arquivo requirements.txt não encontrado!")
        sys.exit(1)
    
    resposta = input("\n📦 Deseja instalar/atualizar dependências? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        instalar_dependencias()
    
    print("\n" + "=" * 60)
    iniciar_aplicacao()


if __name__ == "__main__":
    main()
