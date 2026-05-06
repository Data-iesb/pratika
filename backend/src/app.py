import json
import os
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
table = dynamodb.Table(os.environ["TABLE_NAME"])
topic_arn = os.environ["TOPIC_ARN"]


def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        nome = body.get("nome", "").strip()
        email = body.get("email", "").strip()
        mensagem = body.get("mensagem", "").strip()

        if not nome or not email or not mensagem:
            return response(400, {"error": "Todos os campos são obrigatórios"})

        item = {
            "id": str(uuid.uuid4()),
            "nome": nome,
            "email": email,
            "mensagem": mensagem,
            "data": datetime.utcnow().isoformat(),
        }

        table.put_item(Item=item)

        sns.publish(
            TopicArn=topic_arn,
            Subject=f"Novo contato Prátika: {nome}",
            Message=f"Nome: {nome}\nEmail: {email}\n\nMensagem:\n{mensagem}",
        )

        return response(200, {"message": "Mensagem enviada com sucesso!"})
    except Exception as e:
        return response(500, {"error": str(e)})


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }
