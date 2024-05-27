import os
from flask import Flask, request, jsonify
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI 
from langchain_experimental.tools import PythonREPLTool
from elasticapm.contrib.flask import ElasticAPM
from elasticsearch import Elasticsearch
from logging_es.elastic_connector import log_to_elasticsearch
from langchain_core.prompts import PromptTemplate
from datetime import datetime


import os, json

app = Flask(__name__)

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'demo-ai-search" ',
    'SECRET_TOKEN': '',
    'SERVER_URL': 'http://localhost:8200'
}

apm = ElasticAPM(app)

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)


@app.route("/chat/completions", methods=["POST"])
def openai_proxy():
    # Extract OpenAI client.chat.completions parameters
    data = request.get_json()
    messages = data.get("messages", [])
    response_content = ""

    # Langchain agent to calculate results
    tools = [PythonREPLTool()]
    #llm = ChatOpenAI(base_url="http://192.168.0.140:4000")
    llm = ChatOpenAI()

    # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, stream=True)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # Run the agent
    response = agent_executor.invoke(
    {
        "input": messages,
        "chat_history": ""
    })

    response_content = response["output"]

    print("------DEBUG1--------")
    print(response)
    print(response_content)
    print("------DEBUG1--------")

    # Prepare log data for ES
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    log_data = {
       "request": {"messages": messages[-1]},
       "response": response_content, 
       "timestamp": date_time
        }
    log = json.dumps(log_data)

    print("------DEBUG2--------")
    print(log)
    print("------DEBUG2--------")

    
    apm.capture_message(log_data)
    log_to_elasticsearch(log)

    # Calculate token usage
    prompt_tokens = sum(len(message) for message in messages)
    completion_tokens = len(response)
    total_tokens = prompt_tokens + completion_tokens

    # Based on the results, create a OpenAI client.chat.completions response
    return jsonify(
        {
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                    "content": [response],
                    "role": "assistant"
                },
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens":  total_tokens,
            },
        }
    )




# Start the development server
if __name__ == "__main__":
    app.run( port=5000)
