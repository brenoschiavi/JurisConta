"""
JurisConta - Interface Gráfica
Calculadora de Prazos Processuais com interface moderna
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional


class CalculadoraPrazosGUI:
    """Interface gráfica para calculadora de prazos"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("JurisConta - Calculadora de Prazos Processuais")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Define estilo
        self.setup_styles()
        
        # Carrega feriados
        self.carregar_feriados()
        
        # Cria interface
        self.criar_interface()
    
    def setup_styles(self):
        """Configura estilos visuais"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuração de cores
        self.cores = {
            'primaria': '#2c3e50',
            'secundaria': '#3498db',
            'sucesso': '#27ae60',
            'perigo': '#e74c3c',
            'alerta': '#f39c12',
            'info': '#17a2b8',
            'fundo': '#ecf0f1',
            'branco': '#ffffff'
        }
    
    def carregar_feriados(self):
        """Carrega feriados do arquivo JSON"""
        try:
            with open('feriados.json', 'r', encoding='utf-8') as f:
                self.feriados = json.load(f)
        except FileNotFoundError:
            self.feriados = {
                'nacionais': [],
                'moveis': [],
                'estaduais': {},
                'municipais': {}
            }
    
    def calcular_pascoa(self, ano: int) -> datetime:
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
    
    def calcular_feriados_moveis(self, ano: int):
        """Calcula feriados móveis"""
        pascoa = self.calcular_pascoa(ano)
        carnaval = pascoa - timedelta(days=47)
        corpus_christi = pascoa + timedelta(days=60)
        sexta_santa = pascoa - timedelta(days=2)
        
        return {
            'carnaval': carnaval.strftime('%d/%m/%Y'),
            'carnaval_segunda': (carnaval + timedelta(days=1)).strftime('%d/%m/%Y'),
            'sexta_santa': sexta_santa.strftime('%d/%m/%Y'),
            'pascoa': pascoa.strftime('%d/%m/%Y'),
            'corpus_christi': corpus_christi.strftime('%d/%m/%Y')
        }
    
    def e_feriado(self, data: datetime, estado: str = '', municipio: str = '') -> bool:
        """Verifica se é feriado"""
        data_str = data.strftime('%d/%m')
        data_completa = data.strftime('%d/%m/%Y')
        
        # Verifica feriados móveis
        for feriado in self.feriados.get('moveis', []):
            if feriado['data'] == data_completa:
                return True
        
        # Verifica nacionais
        for feriado in self.feriados.get('nacionais', []):
            if feriado['data'] == data_str:
                return True
        
        # Verifica estaduais
        if estado and estado in self.feriados.get('estaduais', {}):
            for feriado in self.feriados['estaduais'][estado]:
                if feriado['data'] == data_str:
                    return True
        
        # Verifica municipais
        if municipio and municipio in self.feriados.get('municipais', {}):
            for feriado in self.feriados['municipais'][municipio]:
                if feriado['data'] == data_str:
                    return True
        
        return False
    
    def e_dia_util(self, data: datetime, estado: str = '', municipio: str = '') -> bool:
        """Verifica se é dia útil"""
        if data.weekday() in [5, 6]:  # Sábado ou Domingo
            return False
        return not self.e_feriado(data, estado, municipio)
    
    def calcular_prazo(self, data_publicacao: str, prazo_dias: int, 
                      tipo_prazo: str, estado: str = '', municipio: str = '') -> Dict:
        """Calcula o prazo"""
        try:
            data_pub = datetime.strptime(data_publicacao, '%d/%m/%Y')
            data_inicio = data_pub + timedelta(days=1)
            
            # Ajusta para primeiro dia útil
            while not self.e_dia_util(data_inicio, estado, municipio):
                data_inicio += timedelta(days=1)
            
            data_vencimento = data_inicio
            
            if tipo_prazo == 'uteis':
                dias_contados = 0
                while dias_contados < prazo_dias:
                    if self.e_dia_util(data_vencimento, estado, municipio):
                        dias_contados += 1
                    if dias_contados < prazo_dias:
                        data_vencimento += timedelta(days=1)
            else:
                data_vencimento += timedelta(days=prazo_dias - 1)
                while not self.e_dia_util(data_vencimento, estado, municipio):
                    data_vencimento += timedelta(days=1)
            
            hoje = datetime.now().date()
            dias_restantes = (data_vencimento.date() - hoje).days
            
            return {
                'data_inicio': data_inicio.strftime('%d/%m/%Y'),
                'data_vencimento': data_vencimento.strftime('%d/%m/%Y'),
                'dia_semana': self.obter_dia_semana(data_vencimento),
                'dias_restantes': dias_restantes,
                'status': self.obter_status(dias_restantes)
            }
        except ValueError:
            return {'erro': 'Data inválida. Use o formato dd/mm/aaaa'}
    
    def obter_dia_semana(self, data: datetime) -> str:
        """Retorna dia da semana"""
        dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 
                'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
        return dias[data.weekday()]
    
    def obter_status(self, dias_restantes: int) -> str:
        """Retorna status do prazo"""
        if dias_restantes < 0:
            return 'VENCIDO'
        elif dias_restantes == 0:
            return 'VENCE HOJE'
        elif dias_restantes <= 3:
            return 'VENCE EM BREVE'
        else:
            return 'DENTRO DO PRAZO'
    
    def criar_interface(self):
        """Cria a interface gráfica"""
        # Header
        header = tk.Frame(self.root, bg=self.cores['primaria'], height=100)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        title = tk.Label(header, text="⚖ JURISCONTA", 
                        font=('Arial', 28, 'bold'), 
                        bg=self.cores['primaria'], 
                        fg='white')
        title.pack(pady=20)
        
        subtitle = tk.Label(header, text="Calculadora de Prazos Processuais - Baseada no CPC", 
                           font=('Arial', 12), 
                           bg=self.cores['primaria'], 
                           fg='#ecf0f1')
        subtitle.pack()
        
        # Container principal
        container = tk.Frame(self.root, bg=self.cores['fundo'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Formulário
        self.criar_formulario(container)
    
    def criar_formulario(self, parent):
        """Cria formulário de cálculo"""
        # Frame do formulário
        form_frame = tk.LabelFrame(parent, text="Dados do Processo", 
                                  font=('Arial', 14, 'bold'),
                                  bg=self.cores['branco'],
                                  fg=self.cores['primaria'],
                                  padx=20, pady=20)
        form_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Data de publicação
        tk.Label(form_frame, text="📅 Data da Publicação:", 
                font=('Arial', 11), bg=self.cores['branco']).grid(row=0, column=0, sticky='w', pady=10)
        self.data_pub = tk.Entry(form_frame, font=('Arial', 11), width=20)
        self.data_pub.grid(row=0, column=1, sticky='w', padx=10, pady=10)
        self.data_pub.insert(0, datetime.now().strftime('%d/%m/%Y'))
        tk.Label(form_frame, text="(dd/mm/aaaa)", 
                font=('Arial', 9), bg=self.cores['branco'], fg='#7f8c8d').grid(row=0, column=2, sticky='w')
        
        # Prazo em dias
        tk.Label(form_frame, text="📌 Prazo em Dias:", 
                font=('Arial', 11), bg=self.cores['branco']).grid(row=1, column=0, sticky='w', pady=10)
        self.prazo_dias = tk.Entry(form_frame, font=('Arial', 11), width=20)
        self.prazo_dias.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        
        # Tipo de prazo
        tk.Label(form_frame, text="⏱️ Tipo de Prazo:", 
                font=('Arial', 11), bg=self.cores['branco']).grid(row=2, column=0, sticky='w', pady=10)
        self.tipo_prazo = tk.StringVar(value='uteis')
        tk.Radiobutton(form_frame, text="Dias Úteis", variable=self.tipo_prazo, 
                      value='uteis', font=('Arial', 11), bg=self.cores['branco']).grid(row=2, column=1, sticky='w', padx=10)
        tk.Radiobutton(form_frame, text="Dias Corridos", variable=self.tipo_prazo, 
                      value='corridos', font=('Arial', 11), bg=self.cores['branco']).grid(row=3, column=1, sticky='w', padx=10)
        
        # Estado
        tk.Label(form_frame, text="🏛️ Estado (Opcional):", 
                font=('Arial', 11), bg=self.cores['branco']).grid(row=4, column=0, sticky='w', pady=10)
        self.estado = ttk.Combobox(form_frame, font=('Arial', 11), width=30)
        self.estado['values'] = sorted(list(self.feriados.get('estaduais', {}).keys()))
        self.estado.grid(row=4, column=1, sticky='w', padx=10, pady=10)
        
        # Município
        tk.Label(form_frame, text="🏙️ Município (Opcional):", 
                font=('Arial', 11), bg=self.cores['branco']).grid(row=5, column=0, sticky='w', pady=10)
        self.municipio = ttk.Combobox(form_frame, font=('Arial', 11), width=30)
        self.municipio['values'] = sorted(list(self.feriados.get('municipais', {}).keys()))
        self.municipio.grid(row=5, column=1, sticky='w', padx=10, pady=10)
        
        # Botão calcular
        btn_frame = tk.Frame(parent, bg=self.cores['fundo'])
        btn_frame.pack(fill='x')
        
        btn_calcular = tk.Button(btn_frame, text="CALCULAR PRAZO", 
                                font=('Arial', 14, 'bold'),
                                bg=self.cores['secundaria'],
                                fg='white',
                                cursor='hand2',
                                padx=30, pady=15,
                                command=self.calcular)
        btn_calcular.pack(side='left', padx=10)
        
        btn_limpar = tk.Button(btn_frame, text="Limpar", 
                              font=('Arial', 12),
                              bg=self.cores['alerta'],
                              fg='white',
                              cursor='hand2',
                              padx=20, pady=10,
                              command=self.limpar_formulario)
        btn_limpar.pack(side='right', padx=10)
    
    def calcular(self):
        """Executa cálculo do prazo"""
        try:
            data_pub = self.data_pub.get()
            prazo = int(self.prazo_dias.get())
            tipo = self.tipo_prazo.get()
            estado = self.estado.get()
            municipio = self.municipio.get()
            
            resultado = self.calcular_prazo(data_pub, prazo, tipo, estado, municipio)
            
            if 'erro' in resultado:
                messagebox.showerror("Erro", resultado['erro'])
                return
            
            self.exibir_resultado(resultado)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
    
    def exibir_resultado(self, resultado: Dict):
        """Exibe resultado em nova janela"""
        janela_resultado = tk.Toplevel(self.root)
        janela_resultado.title("Resultado do Cálculo")
        janela_resultado.geometry("600x500")
        janela_resultado.configure(bg=self.cores['fundo'])
        
        # Título
        titulo = tk.Label(janela_resultado, text="📊 RESULTADO DO CÁLCULO", 
                         font=('Arial', 18, 'bold'),
                         bg=self.cores['fundo'],
                         fg=self.cores['primaria'])
        titulo.pack(pady=20)
        
        # Frame do resultado
        result_frame = tk.Frame(janela_resultado, bg=self.cores['branco'], padx=30, pady=30)
        result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Determina cor do status
        status = resultado['status']
        if 'VENCIDO' in status or 'VENCE HOJE' in status:
            cor = self.cores['perigo']
        elif 'VENCE EM BREVE' in status:
            cor = self.cores['alerta']
        else:
            cor = self.cores['sucesso']
        
        # Display dos resultados
        resultados = [
            ("📅 Data de Publicação:", self.data_pub.get()),
            ("📆 Início da Contagem:", resultado['data_inicio']),
            ("⏰ Data de Vencimento:", resultado['data_vencimento']),
            ("📆 Dia da Semana:", resultado['dia_semana'].title()),
            ("⏳ Dias Restantes:", f"{resultado['dias_restantes']} dias"),
            ("🔔 Status:", resultado['status'])
        ]
        
        for i, (label, valor) in enumerate(resultados):
            tk.Label(result_frame, text=label, font=('Arial', 12, 'bold'),
                    bg=self.cores['branco']).grid(row=i, column=0, sticky='w', pady=10, padx=10)
            tk.Label(result_frame, text=valor, font=('Arial', 12),
                    bg=self.cores['branco'], fg=cor if i == 5 else 'black').grid(row=i, column=1, sticky='w', pady=10)
        
        # Alerta se necessário
        if resultado['dias_restantes'] < 0:
            tk.Label(result_frame, 
                    text=f"⚠️ ATENÇÃO: O prazo venceu há {abs(resultado['dias_restantes'])} dias!",
                    font=('Arial', 11, 'bold'),
                    bg=self.cores['perigo'],
                    fg='white').grid(row=6, column=0, columnspan=2, pady=20, sticky='ew')
        elif resultado['dias_restantes'] <= 3:
            tk.Label(result_frame, 
                    text="⚠️ ATENÇÃO: Prazo vencendo em breve!",
                    font=('Arial', 11, 'bold'),
                    bg=self.cores['alerta'],
                    fg='white').grid(row=6, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Botão fechar
        btn_fechar = tk.Button(janela_resultado, text="Fechar", 
                              font=('Arial', 12),
                              bg=self.cores['primaria'],
                              fg='white',
                              cursor='hand2',
                              padx=30, pady=10,
                              command=janela_resultado.destroy)
        btn_fechar.pack(pady=20)
    
    def limpar_formulario(self):
        """Limpa campos do formulário"""
        self.data_pub.delete(0, 'end')
        self.data_pub.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.prazo_dias.delete(0, 'end')
        self.tipo_prazo.set('uteis')
        self.estado.set('')
        self.municipio.set('')


def main():
    root = tk.Tk()
    app = CalculadoraPrazosGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

