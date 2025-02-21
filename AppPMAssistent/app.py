from flask import Flask, request, jsonify
import openai
import pandas as pd

app = Flask(__name__)

# Configurar API da OpenAI (ou outro modelo de IA)
openai.api_key = "SUA_CHAVE_OPENAI"

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
    data = request.json
    user_message = data.get("mensagem", "").lower()
    response = knowledge_base.get("fluxo generico", "🤖 Não encontrei um fluxo específico. Pode detalhar melhor sua necessidade?")
    
    for key in knowledge_base:
        if key in user_message:
            response = knowledge_base[key]
            break
    
    return jsonify({"resposta": response})

if __name__ == "__main__":
    app.run(debug=True)