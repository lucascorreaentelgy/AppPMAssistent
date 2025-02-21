from flask import Flask, request, jsonify
import os
import openai
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "Assistente PM rodando com sucesso!"})

# Base de conhecimento para fluxos
knowledge_base = {
    "kpi": "📊 Para definir KPIs, considere: Early-stage → Adoção, Growth → Retenção, Mature → Expansão.",
    "priorizar funcionalidades": "⚖️ Use RICE, MoSCoW ou Eisenhower para priorização.",
    "roadmap": "🛣️ Modelos recomendados: Now-Next-Later, Lean Roadmap.",
    "discovery": "🔍 Use Double Diamond ou JTBD para Product Discovery.",
    "reunião": "📅 Sugestões para Dailies, Retrospectives e Planning Meetings.",
    "benchmark": "📈 Ferramentas: SimilarWeb, Google Trends e Sensor Tower."
}

@app.route("/assistente", methods=["POST"])
def assistente():
    try:
        data = request.get_json()
        if not data or "mensagem" not in data or "api_key" not in data:
            return jsonify({"erro": "Campos 'mensagem' e 'api_key' são obrigatórios"}), 400
        
        openai.api_key = data["api_key"]  # Define a API Key vinda no JSON
        user_message = data["mensagem"].lower()
        
        # Verificar se a mensagem corresponde a um fluxo predefinido
        response = knowledge_base.get("fluxo generico", "🤖 Não encontrei um fluxo específico. Pode detalhar melhor sua necessidade?")
        
        for key in knowledge_base:
            if key in user_message:
                response = knowledge_base[key]
                break
        
        # Se nenhuma resposta predefinida for encontrada, chama o GPT-4
        if response == "🤖 Não encontrei um fluxo específico. Pode detalhar melhor sua necessidade?":
            resposta_gpt = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}]
            )
            response = resposta_gpt["choices"][0]["message"]["content"]
        
        return jsonify({"resposta": response})
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render define automaticamente a porta
    app.run(host="0.0.0.0", port=port, debug=True)
