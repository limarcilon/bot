import os
from flask import Flask, request, jsonify
import slack_sdk
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Variáveis de ambiente para autenticação
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')  # Bot OAuth Token do Slack
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    # Verificação de URL durante a configuração do evento
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Processar eventos de reactions
    if "event" in data:
        event = data["event"]

        # Verifica se é um evento de reaction
        if event.get('type') == 'reaction_added':
            channel = event.get('item', {}).get('channel')
            timestamp = event.get('item', {}).get('ts')
            reaction = event.get('reaction')

            try:
                # Adiciona uma reaction na mensagem
                slack_client.reactions_add(
                    channel=channel,
                    name="thumbsup",  # Reação que você deseja adicionar
                    timestamp=timestamp
                )
            except SlackApiError as e:
                print(f"Help - Error adding reaction: {e.response['error']}")

        # Outros eventos podem ser processados da mesma maneira
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=5000)
