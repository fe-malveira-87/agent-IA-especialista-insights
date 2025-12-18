import traceback
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from app.config import bq_client

# Variável global para logs
query_logs = []

def get_logs():
    return query_logs

def clear_logs():
    global query_logs
    query_logs.clear()

def execute_bigquery_query(sql_query: str):
    """Executa SQL no BigQuery e retorna Markdown."""
    clean_query = sql_query.replace("```sql", "").replace("```", "").strip()
    log_entry = {"sql": clean_query, "status": "pending", "error": None}
    
    print(f"\n--- EXECUTANDO SQL ---\n{clean_query}\n")
    
    try:
        query_job = bq_client.query(clean_query)
        df = query_job.to_dataframe()
        log_entry["status"] = "success"
        query_logs.append(log_entry)
        
        if df.empty:
            return "RESULTADO: 0 linhas. Avise que não há dados."
        
        return df.head(50).to_markdown(index=False)
        
    except Exception as e:
        log_entry["status"] = "error"
        log_entry["error"] = str(e)
        query_logs.append(log_entry)
        return f"ERRO SQL: {str(e)}"

def tool_forecast_ml():
    """
    Gera uma projeção avançada de vendas para os próximos 12 meses.
    Usa Scikit-Learn (Regressão Linear) para tendência + Ajuste de Sazonalidade mensal.
    Compara o projetado com o realizado do ano anterior (YoY).
    """
    print("\n--- ACIONANDO IA PREDITIVA (ML) COM COMPARATIVO YOY ---")
    try:
        # 1. Busca dados históricos (últimos 36 meses para pegar sazonalidade completa)
        sql = """
        SELECT 
            EXTRACT(YEAR FROM DTMOVIMENTO) as ano, 
            EXTRACT(MONTH FROM DTMOVIMENTO) as mes, 
            SUM(valcontabil) as total
        FROM `prj-juma-farol360-poc.GOLD_JUMA.VW_NF_SAIDAS`
        WHERE DTMOVIMENTO >= DATE_SUB(CURRENT_DATE(), INTERVAL 36 MONTH)
        GROUP BY 1, 2 ORDER BY 1, 2
        """
        df = bq_client.query(sql).to_dataframe()
        
        if df.empty or len(df) < 12:
            return "ERRO: Histórico insuficiente para Machine Learning e Comparativo YoY (mínimo 12 meses)."

        # Dicionário de busca rápida para o YoY (Chave: "ano-mes", Valor: Total)
        historico_map = {(r['ano'], r['mes']): r['total'] for _, r in df.iterrows()}

        # 2. Engenharia de Features
        df['idx_tempo'] = range(1, len(df) + 1)
        media_global = df['total'].mean()
        sazonalidade = df.groupby('mes')['total'].mean() / media_global
        df['fator_sazonal'] = df['mes'].map(sazonalidade)
        df['total_limpo'] = df['total'] / df['fator_sazonal']

        # 3. Treina Modelo
        modelo = LinearRegression()
        modelo.fit(df[['idx_tempo']], df['total_limpo'])

        # 4. Projeta Futuro (12 meses)
        ultimo_idx = df['idx_tempo'].max()
        futuro_idx = np.array(range(ultimo_idx + 1, ultimo_idx + 13)).reshape(-1, 1)
        predicao_tendencia = modelo.predict(futuro_idx)

        # 5. Formata Tabela Markdown
        ultimo_ano = int(df['ano'].iloc[-1])
        ultimo_mes = int(df['mes'].iloc[-1])
        
        resultados = []
        resultados.append("| Mês/Ano | Projeção (R$) | YoY (vs Ano Ant.) | Cenário |")
        resultados.append("|---|---|---|---|")
        
        mes_iter = ultimo_mes
        ano_iter = ultimo_ano
        soma_projetada_12m = 0
        soma_anterior_12m = 0

        for val_tendencia in predicao_tendencia:
            mes_iter += 1
            if mes_iter > 12:
                mes_iter = 1
                ano_iter += 1
            
            fator = sazonalidade.get(mes_iter, 1.0) 
            val_final = max(0, val_tendencia * fator)
            
            # Cálculo YoY
            val_ano_anterior = historico_map.get((ano_iter - 1, mes_iter), 0)
            coluna_yoy = "-"
            if val_ano_anterior > 0:
                variacao = ((val_final - val_ano_anterior) / val_ano_anterior) * 100
                coluna_yoy = f"🟢 +{variacao:.1f}%" if variacao > 0 else f"🔴 {variacao:.1f}%"
                soma_anterior_12m += val_ano_anterior
            else:
                coluna_yoy = "🆕 Sem Hist."
            
            soma_projetada_12m += val_final
            resultados.append(f"| {mes_iter:02d}/{ano_iter} | **R$ {val_final/1000:,.1f} K** | {coluna_yoy} | Tendência IA |")

        # Totalização
        var_total = 0
        yoy_total_str = "-"
        if soma_anterior_12m > 0:
             var_total = ((soma_projetada_12m - soma_anterior_12m) / soma_anterior_12m) * 100
             yoy_total_str = f"🟢 **+{var_total:.1f}%**" if var_total > 0 else f"🔴 **{var_total:.1f}%**"

        resultados.append(f"| **TOTAL 12M** | **R$ {soma_projetada_12m/1000000:,.2f} MM** | {yoy_total_str} | **Acumulado** |")

        return "\n".join(resultados)

    except Exception as e:
        traceback.print_exc()
        return f"Erro na execução do ML: {str(e)}"