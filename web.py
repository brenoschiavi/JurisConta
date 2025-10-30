"""
JurisConta - Versão Web
Calculadora de Prazos Processuais com interface web moderna usando Streamlit
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict

# Configuração da página
st.set_page_config(
    page_title="JurisConta - Calculadora de Prazos",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #ecf0f1;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #3498db;
            color: white;
            font-weight: bold;
            font-size: 1.1rem;
            padding: 0.75rem;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_feriados():
    """Carrega feriados do arquivo JSON"""
    try:
        with open('feriados.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'nacionais': [],
            'moveis': [],
            'estaduais': {},
            'municipais': {}
        }


def calcular_pascoa(ano: int) -> datetime:
    """Calcula data da Páscoa"""
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(ano, mes, dia)


def e_feriado(feriados, data: datetime, estado: str = '', municipio: str = '') -> bool:
    """Verifica se é feriado"""
    data_str = data.strftime('%d/%m')
    data_completa = data.strftime('%d/%m/%Y')
    
    # Verifica feriados móveis
    for feriado in feriados.get('moveis', []):
        if feriado.get('data') == data_completa:
            return True
    
    # Verifica nacionais
    for feriado in feriados.get('nacionais', []):
        if feriado.get('data') == data_str:
            return True
    
    # Verifica estaduais
    if estado and estado in feriados.get('estaduais', {}):
        for feriado in feriados['estaduais'][estado]:
            if feriado.get('data') == data_str:
                return True
    
    # Verifica municipais
    if municipio and municipio in feriados.get('municipais', {}):
        for feriado in feriados['municipais'][municipio]:
            if feriado.get('data') == data_str:
                return True
    
    return False


def e_dia_util(feriados, data: datetime, estado: str = '', municipio: str = '') -> bool:
    """Verifica se é dia útil"""
    if data.weekday() in [5, 6]:  # Sábado ou Domingo
        return False
    return not e_feriado(feriados, data, estado, municipio)


def calcular_prazo(feriados, data_publicacao: str, prazo_dias: int, 
                   tipo_prazo: str, estado: str = '', municipio: str = '') -> Dict:
    """Calcula o prazo"""
    try:
        data_pub = datetime.strptime(data_publicacao, '%d/%m/%Y')
        data_inicio = data_pub + timedelta(days=1)
        
        # Ajusta para primeiro dia útil
        while not e_dia_util(feriados, data_inicio, estado, municipio):
            data_inicio += timedelta(days=1)
        
        data_vencimento = data_inicio
        
        if tipo_prazo == 'uteis':
            dias_contados = 0
            while dias_contados < prazo_dias:
                if e_dia_util(feriados, data_vencimento, estado, municipio):
                    dias_contados += 1
                if dias_contados < prazo_dias:
                    data_vencimento += timedelta(days=1)
        else:
            data_vencimento += timedelta(days=prazo_dias - 1)
            while not e_dia_util(feriados, data_vencimento, estado, municipio):
                data_vencimento += timedelta(days=1)
        
        hoje = datetime.now().date()
        dias_restantes = (data_vencimento.date() - hoje).days
        
        dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 
                'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
        
        status = ''
        if dias_restantes < 0:
            status = 'VENCIDO'
        elif dias_restantes == 0:
            status = 'VENCE HOJE'
        elif dias_restantes <= 3:
            status = 'VENCE EM BREVE'
        else:
            status = 'DENTRO DO PRAZO'
        
        return {
            'data_inicio': data_inicio.strftime('%d/%m/%Y'),
            'data_vencimento': data_vencimento.strftime('%d/%m/%Y'),
            'dia_semana': dias[data_vencimento.weekday()],
            'dias_restantes': dias_restantes,
            'status': status
        }
    except ValueError:
        return {'erro': 'Data inválida. Use o formato dd/mm/aaaa'}


def main():
    # Header
    st.markdown('<div style="margin-top: -80px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">⚖️ JURISCONTA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Calculadora de Prazos Processuais - Baseada no CPC</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Carrega feriados
    feriados = carregar_feriados()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Estatísticas")
        stats = {
            'total': len(feriados.get('nacionais', [])) + 
                    len(feriados.get('estaduais', {})) + 
                    len(feriados.get('municipais', {})),
            'estados': len(feriados.get('estaduais', {})),
            'municipios': len(feriados.get('municipais', {}))
        }
        st.metric("Total de Feriados", f"{stats['total']}+")
        st.metric("Estados Cadastrados", f"{stats['estados']}/26")
        st.metric("Municípios Cadastrados", stats['municipios'])
        
        st.markdown("---")
        st.info("ℹ️ Baseado no CPC, Art. 216 - Contagem de prazos")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Dados do Processo")
        
        # Formulário
        data_pub = st.date_input(
            "📅 Data da Publicação",
            value=datetime.now(),
            format="DD/MM/YYYY"
        ).strftime('%d/%m/%Y')
        
        col_a, col_b = st.columns(2)
        with col_a:
            prazo_dias = st.number_input(
                "📌 Prazo em Dias",
                min_value=1,
                value=15,
                step=1
            )
        with col_b:
            tipo_prazo = st.radio(
                "⏱️ Tipo de Prazo",
                ['Dias Úteis', 'Dias Corridos'],
                horizontal=True
            )
        
        # Dropdowns de localização
        estados = sorted(list(feriados.get('estaduais', {}).keys()))
        municipios = sorted(list(feriados.get('municipais', {}).keys()))
        
        col_c, col_d = st.columns(2)
        with col_c:
            estado = st.selectbox(
                "🏛️ Estado (Opcional)",
                [''] + estados
            )
        with col_d:
            municipio = st.selectbox(
                "🏙️ Município (Opcional)",
                [''] + municipios
            )
        
        # Botão calcular
        if st.button("🚀 CALCULAR PRAZO", type="primary"):
            tipo = 'uteis' if tipo_prazo == 'Dias Úteis' else 'corridos'
            resultado = calcular_prazo(feriados, data_pub, prazo_dias, tipo, estado, municipio)
            
            if 'erro' in resultado:
                st.error(f"❌ {resultado['erro']}")
            else:
                st.markdown("---")
                st.header("✅ Resultado do Cálculo")
                
                # Determina cor
                if 'VENCIDO' in resultado['status'] or 'VENCE HOJE' in resultado['status']:
                    color = 'red'
                elif 'VENCE EM BREVE' in resultado['status']:
                    color = 'orange'
                else:
                    color = 'green'
                
                # Exibe resultados
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📅 Data de Publicação", data_pub)
                    st.metric("📆 Início da Contagem", resultado['data_inicio'])
                    st.metric("⏰ Data de Vencimento", resultado['data_vencimento'])
                with col2:
                    st.metric("📆 Dia da Semana", resultado['dia_semana'].title())
                    st.metric("⏳ Dias Restantes", resultado['dias_restantes'], 
                             delta=f"{resultado['status']}")
                    st.markdown(f"### 🔔 Status: :{color}[{resultado['status']}]")
                
                # Alertas
                if resultado['dias_restantes'] < 0:
                    st.error(f"⚠️ ATENÇÃO: O prazo venceu há {abs(resultado['dias_restantes'])} dias!")
                elif resultado['dias_restantes'] <= 3:
                    st.warning("⚠️ ATENÇÃO: Prazo vencendo em breve!")
    
    with col2:
        st.header("ℹ️ Informações")
        
        info_card = f"""
        <div style="background-color: #ecf0f1; padding: 1rem; border-radius: 10px;">
            <h4>📖 Regras CPC</h4>
            <p><b>Art. 216:</b> Contagem excluindo o dia do começo e incluindo o dia do vencimento</p>
            <p><b>§1º:</b> Vencimento em fim de semana ou feriado prorroga para próximo dia útil</p>
            <p><b>§2º:</b> Feriados são considerados dias não úteis</p>
            <p><b>§3º:</b> Contagem inicia no primeiro dia útil após publicação</p>
        </div>
        """
        st.markdown(info_card, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ### 📊 Banco de Dados
        
        - 10 Feriados Nacionais
        - Feriados Móveis (Carnaval, Páscoa, etc.)
        - Feriados Estaduais (26 estados)
        - Feriados Municipais (40+ cidades)
        """)
        
        st.markdown("---")
        
        # Oculta o botão de atualizar
        # if st.button("🔄 Atualizar Banco de Feriados"):
        #     st.cache_data.clear()
        #     st.rerun()


if __name__ == '__main__':
    main()

