import boto3
import json

class ChatAgentResponse:
    def __init__(self, answer: str) -> None:
        self.answer = answer

class ChatAgentService:
    _region = "us-east-1"
    _function_name = "chat-agent"
    _invocation_type = "RequestResponse"

    def __init__(self) -> None:
        self._client = boto3.client(
            service_name="lambda",
            region_name=self._region
        )

    def _parse_agent_response(self, response) -> ChatAgentResponse:
        content = json.loads(response['Payload'].read().decode('utf-8'))
        # The content is already a dictionary, so we don't need to parse it again
        body = content.get('body', {})
        # Check if body is a string (JSON) and parse it if necessary
        if isinstance(body, str):
            body = json.loads(body)
        answer = body.get('answer', '')
        return ChatAgentResponse(answer)

    def invoke_agent(self, query: str, model: str) -> str:
        payload = {
            "query": query,
            "model": model
        }
        response = self._client.invoke(
            FunctionName=self._function_name,
            InvocationType=self._invocation_type,
            Payload=json.dumps(payload)
        )
        chat_response = self._parse_agent_response(response)
        return chat_response.answer
