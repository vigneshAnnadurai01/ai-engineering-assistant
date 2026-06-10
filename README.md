# 📌 MCP-Based Intelligent Account Routing System

## 🚀 Overview

The **MCP (Model Context Pipeline)** System is a modular orchestration framework designed to intelligently process user requests and route them to specialized account-related services.

It acts as a **central decision-making layer** between user input and backend business services, enabling:

- 🧠 Intelligent request routing  
- 🔌 Scalable plugin-based architecture  
- ⚡ Async processing support  
- 🎯 Context-aware tool selection  
- 🧩 Clean separation of concerns  

---

## 🧠 Core Principles

- 🔹 Separation of Concerns  
- 🔹 Plugin-Based Extensibility  
- 🔹 Async Processing Architecture  
- 🔹 Intelligent Routing Engine  
- 🔹 Centralized Orchestration Layer  

---


 

---

## 🔄 Request Processing Lifecycle

### Step 1: User Request
User submits a request through API / UI layer.

### Step 2: MCP Server
Entry point that receives and validates requests.

### Step 3: Request Orchestrator
Coordinates the entire flow and manages routing logic.

### Step 4: Tool Router
Determines which internal system should handle the request.

### Step 5: Intent Classification
Analyzes request intent using classification engine:

- Analytics  
- Assistant  
- Tools  
- General Queries  

### Step 6: Service Execution
Routes request to appropriate domain services:

- Account Services  
- General Services  
- Management Services  

### Step 7: Response Generator
Aggregates outputs and formats final structured response.

### Step 8: Final Response
Returns optimized response to the user.

---

## 🔁 Sequence Flow (Runtime Behavior)

```mermaid id="t3xq9k"
sequenceDiagram
    autonumber
    participant U as User
    participant API as MCP Server
    participant OR as Request Orchestrator
    participant RT as Tool Router
    participant IE as Intent Engine
    participant SV as Service Layer
    participant RG as Response Generator

    U->>API: Send Request
    API->>OR: Validate & Forward Request
    OR->>RT: Route Request
    RT->>IE: Classify Intent

    alt Analytics Request
        IE->>SV: Analytics Service
    else Assistant Request
        IE->>SV: Assistant Service
    else Tools Request
        IE->>SV: Tools Service
    else General Request
        IE->>SV: General Service
    end

    SV->>RG: Process Response
    RG->>U: Final Response