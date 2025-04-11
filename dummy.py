import openai
from dotenv import load_dotenv
import os

from typing_extensions import override
from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):    
    def __init__(self):
        super().__init__()
        self.response_parts = []

    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        self.response_parts.append(delta.value)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

    def get_full_response(self):
        return ''.join(self.response_parts)



def get_response(query: str, thread_id: str,
                assistant_id: str, client: openai.OpenAI) -> str:
    # load_dotenv()
    # client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # assistant_id = os.environ.get("ASSISTANT_ID")

    # Add message to thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query
    )

    # Create a handler instance and stream the response
    handler = EventHandler()
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=handler,
    ) as stream:
        stream.until_done()

    # Return collected string response
    return handler.get_full_response()
