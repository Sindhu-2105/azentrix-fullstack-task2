# Design Document

## Architecture

The system is implemented using LangGraph.

The workflow contains four agents:

1. Triage Agent
2. FAQ Agent
3. Escalation Agent
4. Response Agent

The output of each agent is stored in a shared state object and passed to the next agent.

## Agent Responsibilities

### Triage Agent

Identifies the type of customer issue.

### FAQ Agent

Provides a standard response from the FAQ database.

### Escalation Agent

Checks whether the issue requires escalation to human support.

### Response Agent

Generates the final response returned to the customer.

## Why LangGraph

LangGraph was chosen because it provides a clear way to define agent workflows and manage state transitions between agents.

## Challenges

* Designing agent communication.
* Passing structured data between agents.
* Defining escalation conditions.

## Future Improvements

* Integrate Groq/OpenAI LLMs.
* Connect to a real FAQ database.
* Add sentiment analysis.
* Build a Streamlit web interface.
* Add ticket tracking and logging.

