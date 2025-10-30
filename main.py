"""
JurisConta - Calculadora de Prazos Processuais
Calcula prazos legais considerando CPC, feriados e regras processuais
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import os
import sys

# Cores ANSI para terminal
class Cores:
    """Cores ANSI para formatação no terminal"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Cores principais
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    MAGENTA = '\033[95m'
    
    # Backgrounds
    BG_VERDE = '\033[42m'
    BG_AZUL = '\033[44m'
    BG_AMARELO = '\033[43m'
    BG_VERMELHO = '\033[41m'
    BG_CINZA = '\033[47m'
    BG_CIANO = '\033[46m'


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_titulo(texto: str, cor=Cores.CIANO):
    """Exibe um título formatado"""
    largura = 80
    print(f"\n{cor}{Cores.BOLD}{'='*largura}{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}{texto.center(largura)}{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}{'='*largura}{Cores.RESET}\n")


def exibir_secao(texto: str, cor=Cores.AZUL):
    """Exibe um separador de seção"""
    largura = 80
    print(f"\n{cor}{'─'*largura}{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}{texto.center(largura)}{Cores.RESET}")
    print(f"{cor}{'─'*largura}{Cores.RESET}\n")


def exibir_box(texto: str, cor=Cores.CIANO, largura=76):
    """Exibe texto em uma caixa formatada"""
    linhas = texto.split('\n')
    print(f"{cor}{Cores.BOLD}╔{'═'*largura}╗{Cores.RESET}")
    for linha in linhas:
        print(f"{cor}{Cores.BOLD}║{Cores.RESET} {linha:<{largura}} {cor}{Cores.BOLD}║{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}╚{'═'*largura}╝{Cores.RESET}\n")


def exibir_card(titulo: str, items: List[Dict], cor=Cores.AZUL):
    """Exibe um card com título e lista de itens"""
    largura = 70
    print(f"\n{cor}{Cores.BOLD}┌{'─'*largura}┐{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}│{Cores.RESET} {titulo:<{largura}} {cor}{Cores.BOLD}│{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}├{'─'*largura}┤{Cores.RESET}")
    for item in items:
        chave = item.get('chave', '')
        valor = item.get('valor', '')
        print(f"{cor}{Cores.BOLD}│{Cores.RESET} {chave:.<50} {valor:>18} {cor}{Cores.BOLD}│{Cores.RESET}")
    print(f"{cor}{Cores.BOLD}└{'─'*largura}┘{Cores.RESET}\n")


def exibir_sucesso(texto: str):
    """Exibe mensagem de sucesso"""
    print(f"\n{Cores.VERDE}{Cores.BOLD}✓ {texto}{Cores.RESET}\n")


def exibir_erro(texto: str):
    """Exibe mensagem de erro"""
    print(f"\n{Cores.VERMELHO}{Cores.BOLD}✗ {texto}{Cores.RESET}\n")


def exibir_info(texto: str):
    """Exibe mensagem informativa"""
    print(f"{Cores.CIANO}ℹ {texto}{Cores.RESET}")


def exibir_alerta(texto: str):
    """Exibe mensagem de alerta"""
    print(f"{Cores.AMARELO}{Cores.BOLD}⚠ {texto}{Cores.RESET}")


def input_bonito(prompt: str, cor=Cores.CIANO) -> str:
    """Input com formatação bonita"""
    return input(f"{cor}{Cores.BOLD}→ {prompt}{Cores.RESET} ").strip()


def exibir_menu_item(numero: str, texto: str, descricao: str = "", cor=Cores.AZUL):
    """Exibe um item de menu formatado"""
    if descricao:
        print(f"  {cor}{Cores.BOLD}[{numero}]{Cores.RESET} {texto}")
        print(f"      {Cores.DIM}{descricao}{Cores.RESET}\n")
    else:
        print(f"  {cor}{Cores.BOLD}[{numero}]{Cores.RESET} {texto}\n")


def exibir_logo():
    """Exibe o logo e banner do programa"""
    logo = f"""
{Cores.CIANO}{Cores.BOLD}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    ╦═╗╔═╗╔═╗╔═╗  ╔═╗╔═╗╔═╗╔═╗╦═╗                          ║
║                    ╠╦╝║╣ ║╣ ║ ╦  ║╣ ║  ╚═╗╚═╗╠╦╝                          ║
║                    ╩╚═╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝╩╚═                          ║
║                                                                           ║
║              Calculadora de Prazos Processuais - Baseada no CPC          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Cores.RESET}
"""
    print(logo)

# ... existing code ...
