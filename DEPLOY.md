# 🚀 Como Fazer Deploy do JurisConta na Web

## 📋 Requisitos

- Python 3.8 ou superior
- Conta gratuita em um dos serviços abaixo

## 🌐 Opções de Deploy

### 1. Streamlit Cloud (Recomendado - Grátis e Fácil)

**Passo a passo:**

1. **Criar conta no GitHub**
   - Acesse https://github.com
   - Crie uma conta gratuita

2. **Fazer upload do código**
   - Crie um novo repositório no GitHub
   - Faça upload de todos os arquivos do projeto

3. **Conectar com Streamlit Cloud**
   - Acesse https://share.streamlit.io
   - Faça login com sua conta do GitHub
   - Clique em "New app"
   - Selecione seu repositório
   - Main file path: `web.py`
   - Clique em "Deploy"

4. **Pronto!**
   - Seu app estará online em segundos
   - URL será algo como: `https://seuapp.streamlit.app`

---

### 2. Heroku (Alternativa)

1. **Instalar Heroku CLI**
   - Baixe em: https://devcenter.heroku.com/articles/heroku-cli

2. **Criar arquivos necessários:**
   
   **Procfile:**
   ```
   web: streamlit run web.py --server.port=$PORT --server.address=0.0.0.0
   ```
   
   **runtime.txt:**
   ```
   python-3.11.0
   ```

3. **Deploy:**
   ```bash
   heroku login
   heroku create jurisconta
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

---

### 3. Render (Gratuito)

1. **Criar conta** em https://render.com

2. **New Web Service**
   - Connect repository (GitHub)
   - Environment: Python 3
   - Build command: `pip install -r requirements-web.txt`
   - Start command: `streamlit run web.py --server.port=$PORT`

3. **Deploy automático** a cada push no GitHub

---

## 🏃 Como Rodar Localmente

```bash
# Instalar dependências
pip install streamlit

# Executar aplicação
streamlit run web.py
```

Acesse: http://localhost:8501

---

## 📝 Checklist Antes do Deploy

- [ ] Arquivo `requirements-web.txt` criado
- [ ] Arquivo `web.py` funcional
- [ ] Arquivo `feriados.json` incluído
- [ ] Código versionado no Git (GitHub)
- [ ] Testado localmente

---

## 🔗 Links Úteis

- Streamlit Cloud: https://share.streamlit.io
- Documentação Streamlit: https://docs.streamlit.io
- Heroku: https://www.heroku.com
- Render: https://render.com

---

**Dica:** O Streamlit Cloud é a opção mais simples e recomendada para começar!

