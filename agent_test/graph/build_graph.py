import importlib
from typing import Annotated
from typing import Dict
from typing_extensions import TypedDict

from omegaconf import DictConfig

from langgraph.graph import StateGraph, START, END
from langgraph.graph import CompiledGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agent_test.utils.alias import LLM



class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def build_graph(llm_dict: Dict[str, LLM], cfg: Dict[str, DictConfig]) -> CompiledGraph:
    graph_builder = StateGraph(State)
    tools_dict = {}
    tools_list = set()
    for toolsets in cfg.tools:
        for llm_, tools in toolsets.items():
            llm_tools = []
            for tool_module_name, tool_class_name in tools.items():
                tool_module = importlib.import_module(tool_module_name)
                llm_tools.append(getattr(tool_module, tool_class_name))
            tools_list.update(set(llm_tools))
            tools_dict[llm_] = llm_tools
    if len(tools_list) > 0:
        tool_node = ToolNode(tools=list(tools_list))
        graph_builder.add_node("tools", tool_node)
    for node in cfg.nodes:
        node_module = importlib.import_module(node.module_name)
        graph_builder.add_node(
            node.node_name,
            getattr(node_module, node.class_name)(
                node.params,
                llm_dict.get(node.model, None),
                tools_dict.get(node.model, None),
            ),
        )
    for edge in cfg.edges:
        graph_builder.add_edge(edge.vertex[0], edge.vertex[1])
    graph_builder.add_edge(START, cfg.edges.start_node)
    graph_builder.add_edge(cfg.edges.end_node, END)
    for cedge in cfg.condition_edes:
        cfunc_module = importlib.import_module(cedge.cfunc_module_name)
        graph_builder.add_conditional_edge(
            cedge.node,
            getattr(cfunc_module, cedge.cfunc_name),
            cedge.route,
        )
    return graph_builder.compile()
