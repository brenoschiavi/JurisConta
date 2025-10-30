# JurisConta - Calculadora de Prazos Processuais

Calculadora de prazos processuais baseada no CPC (Código de Processo Civil), similar ao [Prazo Fácil](https://prazofacil.com.br/).

## 📋 Funcionalidades

- ✅ **Cálculo de prazos** baseado nas regras do CPC (art. 216)
- ✅ **Contagem em dias úteis ou corridos**
- ✅ **Banco de feriados completo**:
  - 🗓️ **Feriados móveis** (calculados automaticamente): Carnaval, Sexta-feira Santa, Páscoa, Corpus Christi
  - 🏛️ **10 feriados nacionais** fixos
  - 🏛️ **Feriados estaduais** de todos os 26 estados brasileiros (cobertura 100%)
  - 🏙️ **Feriados municipais** das principais capitais e cidades
  - 📊 **Total: 100+ feriados** cadastrados
- ✅ **Contagem regressiva** e alertas de vencimento
- ✅ **Status visual** do prazo (vencido, vence hoje, vence em breve, dentro do prazo)
- ✅ **Interface via terminal** (linha de comando)
- ✅ **Gerenciamento de feriados** customizados
- ✅ **Estatísticas** do banco de dados de feriados

## 🗓️ Banco de Feriados Completo

O sistema inclui um banco de dados abrangente baseado em fontes oficiais ([feriados.com.br](https://feriados.com.br)):

### Feriados Móveis
Calculados automaticamente com base no algoritmo de Meeus:
- Carnaval (Segunda e Terça-feira)
- Sexta-feira Santa
- Páscoa
- Corpus Christi

### Feriados Nacionais (10)
Todos os feriados nacionais obrigatórios no Brasil.

### Feriados Estaduais (26 estados)
Cobertura completa de todos os estados brasileiros com seus feriados específicos.

### Feriados Municipais (40+ cidades)
Principais capitais e cidades brasileiras incluídas:
- Todas as capitais
- Grandes cidades metropolitanas
- Cidades históricas e turísticas

## 🎯 Como Funciona

### Regras do CPC Implementadas:

- **Art. 216**: O prazo será contado excluindo-se o dia do começo e incluindo-se o dia do vencimento
- **Art. 216, §1º**: Quando o vencimento cair em sábado, domingo ou feriado, o prazo prorroga-se para o primeiro dia útil seguinte
- **Art. 216, §2º**: São considerados dias não úteis os feriados
- **Art. 216, §3º**: A contagem do prazo inicia-se no primeiro dia útil subsequente ao da publicação, intimação ou juntada aos autos

## 🚀 Como Usar

### Instalação

Não requer instalação de dependências! Usa apenas a biblioteca padrão do Python.

### Execução

#### Interface Gráfica (GUI) - Recomendado
```bash
python gui.py
```

#### Interface Terminal (CLI)
```bash
python main.py
```

### Exemplo de Uso

1. Execute o programa
2. Escolha a opção "1. Calcular Prazo"
3. Informe:
   - Data da publicação (dd/mm/aaaa)
   - Prazo em dias
   - Tipo de prazo (úteis ou corridos)
   - Estado e município (opcional, para considerar feriados locais)
   - Matéria do processo

4. Visualize o resultado com:
   - Data de início da contagem
   - Data de vencimento
   - Dia da semana do vencimento
   - Dias restantes
   - Status do prazo

**Exemplo Prático:**
```
📅 Data da publicação (dd/mm/aaaa): 15/12/2024
📌 Prazo em dias: 15
Tipo de prazo: 1. Dias Úteis
🏛️ Estado (opcional): São Paulo
🏙️ Município (opcional): São Paulo
⚖️ Matéria: Cível

RESULTADO:
📅 Data de Publicação: 15/12/2024
📌 Prazo: 15 dias úteis
📆 Início da Contagem: 16/12/2024
⏰ Data de Vencimento: 06/01/2025 (segunda-feira)
⏳ Dias Restantes: 22 dias
🔔 Status: 🟢 DENTRO DO PRAZO
```

### Adicionar Feriados

1. Escolha a opção "2. Adicionar Feriado"
2. Selecione o tipo (estadual ou municipal)
3. Informe o local, data e nome do feriado

## 📁 Estrutura do Projeto

```
JurisConta/
├── gui.py            # Interface gráfica (GUI) - Recomendado
├── main.py           # Interface terminal (CLI)
├── feriados.json     # Banco de dados de feriados
├── requirements.txt  # Dependências (nenhuma)
└── README.md         # Documentação
```

## 🔧 Características Técnicas

- **Linguagem**: Python 3
- **Interface**: GUI (tkinter) e Terminal (CLI)
- **Arquivo de dados**: JSON (feriados.json)
- **Dependências**: Apenas biblioteca padrão Python

## ⚖️ Considerações Legais

Este é um software auxiliar para cálculo de prazos processuais. Sempre consulte as regras específicas do seu tribunal e verifique os calendários oficiais. O sistema é baseado nas regras gerais do CPC, mas podem existir particularidades locais ou regimentais.

## 📝 Licença

Este projeto é de uso livre para fins profissionais e educacionais.

---

**Observação**: A contagem do prazo inicia-se no primeiro dia útil após a publicação.
