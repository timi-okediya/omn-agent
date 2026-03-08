from langchain_core.messages import HumanMessage
from graph import app
from core.state import initial_state

print("Automation Assistant Ready. Type 'exit' to quit.\n")

state = {
    "messages": initial_state["messages"].copy()
}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye.")
        break

    state["messages"].append(HumanMessage(content=user_input))
    state["user_message"] = None

    for event in app.stream(state):
        node_name = list(event.keys())[0]
        node_output = event[node_name]
        
        if "user_message" in node_output and node_output["user_message"]:
            print(f"\n>>> {node_output['user_message']}\n")
        
        state = node_output

    print("Assistant:", state["messages"][-1].content)
