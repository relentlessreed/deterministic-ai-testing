import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


DEFAULT_RESPONSE = "MockLLM default response. Add scenarios/default.yaml rules to customize this."


ScenarioDict = Dict[str, Any]


def load_scenarios(path: str = "scenarios/default.yaml") -> List[ScenarioDict]:
    scenario_path = Path(path)

    if not scenario_path.exists():
        return []

    data = yaml.safe_load(scenario_path.read_text()) or []

    if not isinstance(data, list):
        raise ValueError("Scenario file must contain a YAML list.")

    return data


def normalize_prompt(text: str) -> str:
    return " ".join(text.lower().split())


def find_matching_scenario(
    prompt: str,
    scenarios: List[ScenarioDict],
) -> Optional[ScenarioDict]:
    normalized = normalize_prompt(prompt)

    for scenario in scenarios:
        match = scenario.get("match", {})

        exact = match.get("exact")
        contains = match.get("contains")
        regex = match.get("regex")

        if exact and normalized == normalize_prompt(exact):
            return scenario

        if contains and normalize_prompt(contains) in normalized:
            return scenario

        if regex and re.search(regex, prompt, flags=re.IGNORECASE):
            return scenario

    return None


def messages_to_prompt(messages) -> str:
    return "\n".join(
        [message.content for message in messages if message.content]
    )
