# ai-agent-langgraph

## AI Agent with LangGraph Integration

This project demonstrates an AI agent built using **LangGraph**, **Flask**, and **Python**. It processes user inputs related to product assistance and order management, leveraging a state machine architecture for decision-making.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Directory Structure](#directory-structure)
- [Core Components](#core-components)
  - [Agent State](#agent-state)
  - [Router](#router)
  - [Tool Selector](#tool-selector)
  - [Policy Guard](#policy-guard)
  - [Responder](#responder)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The AI agent processes user queries related to:

- **Product Assistance**: Recommending products based on user input.
- **Order Management**: Handling order-related queries, including cancellations.

The agent utilizes a **state machine model** to manage the flow of information and decisions.

---

## Technologies Used

- **Python 3.x**
- **Flask**: Web framework for building the API.
- **LangGraph**: State machine library for managing agent workflows.
- **Flask-CORS**: Middleware for handling Cross-Origin Resource Sharing.
- **JSON**: Data format for communication.

---

## Setup Instructions

### Prerequisites

Ensure you have **Python 3.8 or higher** installed.

### Clone the Repository

```bash
git clone https://github.com/vikaspathak0911/ai-agent-langgraph.git
cd ai-agent-langgraph
```

## Directory Structure

```text
ai-agent-langgraph/
│
├── app.py               # Flask application entry point
├── graph_enhanced.py    # LangGraph agent definition
├── requirements.txt     # Python dependencies
├── data/                # Directory containing data files
│   └── orders.json      # Sample order data
├── prompts/             # Directory containing prompt templates
├── src/                 # Source code for agent logic
├── tests/               # Unit tests for the application
└── setup_project.sh     # Script for setting up the project environment

```

---

## Core Components

### Agent State

The `AgentState` class manages the state of the agent, including:

- `user_input`: The input received from the user.
- `intent`: The determined intent of the user input.
- `tools_called`: List of tools invoked during the process.
- `evidence`: Collected evidence to support decisions.
- `policy_decision`: Final policy decision made by the agent.
- `final_message`: The response message to be sent to the user.

### Router

The router analyzes the user's input to determine the intent. It categorizes the input into:

- `product_assist`: For product-related queries.
- `order_help`: For order-related queries.
- `other`: For all other queries.

### Tool Selector

Based on the determined intent, the tool selector invokes appropriate tools:

- **Product Assist**: Invokes tools like `product_search`, `size_recommender`, and `eta`.
- **Order Help**: Invokes `order_lookup` to fetch order details.

### Policy Guard

The policy guard evaluates whether the requested action (e.g., order cancellation) is permissible. It checks conditions like:

- Whether the order exists.
- Whether the cancellation is within the allowed time frame.

### Responder

The responder formulates the final message based on the agent's state and decisions. It crafts a response to be sent back to the user.

---

## Running the Application

```bash

pip install -r requirements.txt
python app.py

The application will start on http://127.0.0.1:5500

```

##sample
<img width="1912" height="1048" alt="image" src="https://github.com/user-attachments/assets/fb9be8c5-de9f-4150-8072-77f940ea806d" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/f1774a56-9def-49d1-99ab-88b09e2f98e3" />





