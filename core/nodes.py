from core.state import AgentState


def planner(llm):
    def _node(state: AgentState):
        planning_prompt = f"""
        Break this development task into ordered actionable steps.

        Task:
        {state["messages"][-1].content}

        Return steps as a numbered list.
        """

        response = llm.invoke(planning_prompt)

        steps = [
            s.split(".", 1)[-1].strip()
            for s in response.content.split("\n")
            if s.strip()
        ]

        return {
            "plan": steps,
            "current_step": 0,
            "max_steps": 10,
        }

    return _node


def executor(llm):
    def _node(state: AgentState):
        if state["current_step"] >= len(state["plan"]):
            return {}

        if state["current_step"] >= state["max_steps"]:
            return {
                "messages": [
                    llm.invoke("Execution stopped: max steps reached.")
                ]
            }

        step = state["plan"][state["current_step"]]

        execution_prompt = f"""
        You are executing this step safely:

        Step:
        {step}

        Use tools if necessary.
        """

        response = llm.invoke(execution_prompt)

        return {
            "messages": [response],
            "current_step": state["current_step"] + 1,
        }

    return _node


def review(llm):
    def _node(state: AgentState):
        review_prompt = """
        Review the completed steps.
        Are all steps done correctly?
        If yes, say COMPLETE.
        If not, explain what is missing.
        """

        response = llm.invoke(review_prompt)

        return {"messages": [response]}

    return _node
