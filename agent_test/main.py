import argparse
import logging
import os

from dotenv import load_dotenv
from omegaconf import DictConfig
from omegaconf import OmegaConf

from langchain import HuggingFaceHub
from langgraph.graph import CompiledGraph

from agent_test.graph.build_graph import build_graph
from agent_test.utils.constants import DEFAULT_CFG_PATH


def stream_graph_updates(graph: CompiledGraph, user_input: str) -> None:
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


def main(cfg: DictConfig):
    llm = HuggingFaceHub(
        repo_id = cfg.model, huggingfacehub_api_token = os.getenv(cfg.api_key)
    )
    llm_dict = {"base": llm} # assume I may want to use different models
    graph = build_graph(llm_dict, cfg)

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(graph, user_input)
        except TypeError:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(graph, user_input)
            break

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--cfg",
        default=os.getenv("DEFAULT_CFG_PATH"),
        type=str,
        help="path to the desired config file",
    )
    args = vars(parser.parse_args())
    args = OmegaConf.create({k: v for k, v in args.items() if v is not None})
    main(args)
