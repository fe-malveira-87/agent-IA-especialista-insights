import traceback
import calendar
import random
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.genai import types

# Importações dos nossos módulos
from app.config import genai_client, PORT
import app.prompts as prompts
import app.tools as tools
import app.utils as utils

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Limpa logs antigos
    tools.clear_logs()
    
    try:
        data = request.json
        user_msg = data.get("message", "")
        print(f"User: {user_msg}")

        # --- 2. LÓGICA DE DATA INTELIGENTE (Restaurada) ---
        hj = datetime.now()
        ult_dia_mes = calendar.monthrange(hj.year, hj.month)[1]
        
        # Se for dia 1, 2 ou 3, foca no mês anterior (Fechamento)
        if hj.day <= 3:
            target_month = 12 if hj.month == 1 else hj.month - 1
            target_year = hj.year - 1 if hj.month == 1 else hj.year
            fase_mes = "INÍCIO (FECHAMENTO)"
        else:
            target_month = hj.month
            target_year = hj.year
            fase_mes = "CORRENTE"

        data_ctx = f"HOJE: {hj.strftime('%d/%m/%Y')}. FASE: {fase_mes}. MÊS FOCO: {target_month}/{target_year}. DIAS NO MÊS: {ult_dia_mes}."
        
        # --- 3. LÓGICA DE SUGESTÃO DINÂMICA (Restaurada) ---
        diretriz_extra = ""
        palavras_gatilho = ["insight", "resumo", "geral", "analise", "dashboard", "oi", "ola"]
        temas_especificos = ["estoque", "venda", "faturamento", "produto", "pagar", "ranking"]
        
        msg_lower = user_msg.lower()
        eh_generico = (len(user_msg.split()) < 4 or any(p in msg_lower for p in palavras_gatilho))
        tem_tema_definido = any(t in msg_lower for t in temas_especificos)

        if eh_generico and not tem_tema_definido:
            topics = [
                f"FOCO: Analise o FATURAMENTO acumulado de {hj.year} por LOJA.",
                "FOCO: Analise os ESTOQUES criticos (VW_SALDO_ESTOQUE) dos itens mais vendidos.",
                "FOCO: Analise os TOP PRODUTOS (Curva A) em Vendas do ano.",
                "FOCO: Compare o faturamento deste mês com o mês anterior (VW_NF_SAIDAS).",
            ]
            escolha = random.choice(topics)
            diretriz_extra = f"\n\n[DIRETRIZ DE VARIEDADE]: O usuário pediu algo genérico. Sugestão de foco: {escolha}"
            print(f"--- Sorteio Dinâmico: {escolha} ---")

        # --- 4. Monta Prompt e Configura IA ---
        system_instr = prompts.get_system_prompt(data_ctx, hj.year)
        
        # Concatena a diretriz extra na mensagem do usuário
        full_msg = f"CONTEXTO TEMPORAL: {data_ctx}\n{diretriz_extra}\nPERGUNTA: {user_msg}"

        config_ia = types.GenerateContentConfig(
            temperature=0.4,
            tools=[tools.execute_bigquery_query, tools.tool_forecast_ml],
            system_instruction=[types.Part.from_text(text=system_instr)],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False, maximum_remote_calls=3
            )
        )

        # 5. Chama o Gemini
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Part.from_text(text=full_msg)],
            config=config_ia
        )

        # 6. Processa Resposta
        final_text = "Desculpe, sem resposta."
        if response and response.text:
            final_text = utils.process_response_text(response.text)

        return jsonify({
            "response": final_text,
            "logs": tools.get_logs()
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "logs": tools.get_logs()}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)