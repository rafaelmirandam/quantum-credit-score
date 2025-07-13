import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("QuantumFinance - Demonstração de Score de Crédito para Parceiros")

# --- Configuração da API ---
API_URL = "http://localhost:8000/predict"
# Esta chave deve corresponder à definida na API (quantumfinance_secret_token_12345)
API_KEY = st.text_input("Insira a Chave de API (X-API-KEY)", type="password")

st.header("Insira os Dados do Cliente (Transações Recentes Simuladas)")

# --- Formulário de Entrada ---
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Idade (Age)", value=35.0, step=1.0)
    annual_income = st.number_input("Renda Anual (Annual_Income)", value=70000.0, step=1000.0)
    monthly_salary = st.number_input("Salário Líquido Mensal (Monthly_Inhand_Salary)", value=5500.0, step=100.0)
    outstanding_debt = st.number_input("Dívida Pendente (Outstanding_Debt)", value=1200.0, step=100.0)

with col2:
    num_bank_accounts = st.number_input("Nº de Contas Bancárias (Num_Bank_Accounts)", value=4.0, step=1.0)
    num_credit_card = st.number_input("Nº de Cartões de Crédito (Num_Credit_Card)", value=5.0, step=1.0)
    interest_rate = st.number_input("Taxa de Juros Média (Interest_Rate)", value=15.0, step=1.0)
    utilization_ratio = st.number_input("Taxa de Utilização de Crédito (Credit_Utilization_Ratio)", value=32.5, step=0.1)

with col3:
    num_of_loan = st.number_input("Nº de Empréstimos (Num_of_Loan)", value=2.0, step=1.0)
    delay_due_date = st.number_input("Atraso Médio (dias) (Delay_from_due_date)", value=10.0, step=1.0)
    num_delayed_payment = st.number_input("Nº de Pagamentos Atrasados (Num_of_Delayed_Payment)", value=3.0, step=1.0)
    changed_credit_limit = st.number_input("Mudança no Limite de Crédito (%) (Changed_Credit_Limit)", value=5.0, step=0.5)
    total_emi = st.number_input("Total de Parcelas Mensais (Total_EMI_per_month)", value=300.0, step=10.0)

# --- Chamada da API ---
if st.button("Consultar Score de Crédito"):
    if not API_KEY:
        st.error("Por favor, insira a Chave de API.")
    else:
        payload = {
            "Age": age,
            "Annual_Income": annual_income,
            "Monthly_Inhand_Salary": monthly_salary,
            "Num_Bank_Accounts": num_bank_accounts,
            "Num_Credit_Card": num_credit_card,
            "Interest_Rate": interest_rate,
            "Num_of_Loan": num_of_loan,
            "Delay_from_due_date": delay_due_date,
            "Num_of_Delayed_Payment": num_delayed_payment,
            "Changed_Credit_Limit": changed_credit_limit,
            "Outstanding_Debt": outstanding_debt,
            "Credit_Utilization_Ratio": utilization_ratio,
            "Total_EMI_per_month": total_emi
        }

        headers = {
            "X-API-KEY": API_KEY
        }

        try:
            with st.spinner("Consultando a API segura da QuantumFinance..."):
                response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                st.success("Score Calculado com Sucesso!")
                st.subheader(f"Resultado: {result['credit_score']}")
                st.info(f"Versão do Modelo: {result['model_version']}")
            
            elif response.status_code == 403:
                st.error("Autenticação Falhou (403 Forbidden): Verifique a Chave de API.")
            elif response.status_code == 429:
                st.warning("Throttling Ativado (429 Too Many Requests): Muitas requisições em um curto período. Aguarde um momento.")
            else:
                st.error(f"Erro na API (Status {response.status_code}): {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Falha ao conectar à API. Verifique se o servidor FastAPI está em execução em http://localhost:8000.")