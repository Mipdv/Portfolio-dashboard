from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import pandas as pd
import json
import plotly
import plotly.express as px
import requests
import time

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    msg = Message('New Message!', sender=os.getenv('MAIL_USERNAME'), recipients=[os.getenv('MAIL_USERNAME')])
    msg.body = f"Message from: {email}\n{subject}\n\n{message}"
    mail.send(msg)
    return redirect(url_for('index') + "#contact-me")

# ... (início da rota @app.route("/dashboard") e imports)

# ... (início da rota @app.route("/dashboard") e imports)

@app.route("/dashboard")
def dash():
    # --- 1. Leitura do Arquivo Excel (XLSX) ---
    FILE_PATH = "civil_court.xlsx"
    
    try:
        # Lê o arquivo. A linha com os anos (2023, 2024) é a 4ª linha (índice 3).
        df_wide = pd.read_excel(
            FILE_PATH,
            header=3,
            # Não usaremos skiprows aqui para evitar confusão de índice.
            # Apenas garantimos que o header está na linha correta.
        )
    except Exception as e:
        return f"Erro ao ler o arquivo XLSX: Verifique o caminho ou o parâmetro 'header'. Erro: {e}"

    # ⚠️ CORREÇÃO CRÍTICA 1: Remove a linha "Total" (que é a primeira linha de dados)
    # A linha 'Total' é sempre a primeira linha após o cabeçalho.
    df_wide = df_wide.iloc[1:].copy()
    
    # ⚠️ CORREÇÃO CRÍTICA 2: Seleção Explícita e Correta das Colunas Filed (Arquivados)
    # Colunas: [0]District, [1]Filed_2023, [2]Filed_2024
    df_wide = df_wide.iloc[:, [0, 1, 2]].copy()
    
    # Renomeação
    df_wide.rename(columns={
        df_wide.columns[0]: 'District',
        df_wide.columns[1]: 'Filed_2023', 
        df_wide.columns[2]: 'Filed_2024'
    }, inplace=True)
    
    # -------------------------------------------------------------
    # O CÓDIGO DE LIMPEZA E MELT ANTERIOR PODE SER MANTIDO AQUI:
    # -------------------------------------------------------------

    value_cols = ['Filed_2023', 'Filed_2024']
    
    for col in value_cols:
        df_wide[col] = df_wide[col].astype(str).str.replace(',', '').str.replace(' ', '')
        df_wide[col] = df_wide[col].str.extract('(\d+\.?\d*)', expand=False)
        df_wide[col] = pd.to_numeric(df_wide[col], errors='coerce')
    
    df_wide.dropna(subset=['District'] + value_cols, inplace=True)

    # --- 3. TRANSFORMAÇÃO PARA FORMATO LONGO (pd.melt) ---
    df_long = pd.melt(
        df_wide,
        id_vars=['District'],
        value_vars=value_cols,
        var_name='Ano',
        value_name='Casos Arquivados'
    )
    
    df_long['Ano'] = df_long['Ano'].str.replace('Filed_', '')

    # --- 4. Geração do Plotly ---
    fig1 = px.bar(
        df_long, 
        x='District',
        y='Casos Arquivados',
        color='Ano',
        barmode='group',
        title="Casos Civis Arquivados por Distrito (2023 vs 2024)",
        labels={'District': 'Circuito e Distrito', 'Casos Arquivados': 'Número de Casos'}
    )

    print(df_wide.head(10))
    
    fig1.update_layout(xaxis={'categoryorder': 'total descending', 'tickangle': 45})

    # --- 5. Retorno Flask ---
    graph1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dashboard.html", graph1=graph1)
if __name__ == "__main__":
    app.run(debug=True)#nao comitar!!