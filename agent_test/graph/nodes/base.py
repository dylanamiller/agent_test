from typing import Dict
from typing import List
from typing import Optional

from omegaconf import DictConfig

from agent_test.utils.alias import LLM
from agent_test.utils.alias import State
from agent_test.utils.alias import Tool


class BaseNode:
    def __init__(
        self,
        cfg: DictConfig,
        llm: Optional[LLM] = None,
        tools: Optional[List[Tool]] = None
    ):
        self._llm = llm

    def __call__(self, state: State) -> Dict[str, List[str]]:
        # include cusotm logic
        messages = state["messages"]
        response = self._llm.invoke(messages)
        return {"messages": [response]}
