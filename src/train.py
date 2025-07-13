import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler

# Configuração do MLflow
mlflow.set_experiment("QuantumFinance_Partner_Score")

def train_model():
    # 1. Carregar os dados
    # Substitua pelo caminho real do dataset baixado do Kaggle
    try:
        df = pd.read_csv("../data/raw/train.csv")
    except FileNotFoundError:
        print("Erro: Dataset não encontrado. Baixe de https://www.kaggle.com/datasets/parisrohan/credit-score-classification")
        return

    # 2. Pré-processamento Simplificado (Foco em features relevantes para o exemplo)
    features = [
        'Age', 'Annual_Income', 'Monthly_Inhand_Salary',
        'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate',
        'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment',
        'Changed_Credit_Limit', 'Outstanding_Debt', 'Credit_Utilization_Ratio',
        'Total_EMI_per_month'
    ]
    target = 'Credit_Score'

    # Limpeza simples de nulos (substituir pela média para este exemplo)
    for col in features:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col].fillna(df[col].median(), inplace=True)

    X = df[features]
    y = df[target]

    # Escalonamento de features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=features)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

    # 3. Treinamento e Rastreamento com MLflow
    with mlflow.start_run(run_name="RandomForest_Baseline"):
        n_estimators = 100
        max_depth = 10

        # Log de Parâmetros
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("features_used", features)

        # Treinamento do modelo
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)

        # Predições e Métricas
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')

        # Log de Métricas
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision_weighted", precision)
        mlflow.log_metric("recall_weighted", recall)

        print(f"Modelo treinado. Acurácia: {accuracy:.4f}")

        # Log do Modelo (Artefato)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="credit_score_model",
            registered_model_name="QuantumCreditScore"
        )

        # Log do Scaler (Importante para a API)
        mlflow.sklearn.log_model(scaler, "scaler")

if __name__ == '__main__':
    train_model()