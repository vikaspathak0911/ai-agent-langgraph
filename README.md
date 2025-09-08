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

# Create a new environment with Python 3.9
conda create -n ai_agent python=3.9 -y

# Activate the environment
conda activate ai_agent

# install pip in the environment if it's not already:
conda install pip -y

# Then install your requirements:
pip install -r requirements.txt

|----------------------------------------------------------------------
|		# Run app.py file buil with flask
|		python app.py
|
|		# Open index.html file on web browser or live preview on VS code
|		# Pass the query to the ChatBot
|---------------------------------------------------------------------
								
								OR
			
|--------------------------------------------------------------------			
|		# if you want to test all 4 test cases provided above 
|		cd tests
|		python test_cases.py
|----------------------------------------------------------------------

```

##sample
<img width="1912" height="1048" alt="image" src="https://github.com/user-attachments/assets/fb9be8c5-de9f-4150-8072-77f940ea806d" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/f1774a56-9def-49d1-99ab-88b09e2f98e3" />
<img width="1920" height="1080" alt="Screenshot (652)" src="https://github.com/user-attachments/assets/570b50bd-0bc3-4749-bba5-de27db5f10ad" />

<img width="1920" height="1080" alt="Screenshot (654)" src="https://github.com/user-attachments/assets/dc03e36f-4164-4552-bb9a-2dd2eb7016f4" />

<img width="1920" height="1080" alt="Screenshot (655)" src="https://github.com/user-attachments/assets/d462dbe1-3b05-43b5-b672-945bd71e79e9" />











