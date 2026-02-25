# groq api => 
from langchain_core.messages import HumanMessage
from core.graph import app
from core.state import initial_state

print("Automation Assistant Ready. Type 'exit' to quit.\n")

# Create working state copy
state = {
    "messages": initial_state["messages"].copy()
}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye.")
        break

    # Add user message
    state["messages"].append(HumanMessage(content=user_input))

    # Run graph
    state = app.invoke(state)

    # Print last assistant message
    print("Assistant:", state["messages"][-1].content)
