import re
from pathlib import Path
from typing import List, Optional

import yaml

from app.models import Scenario


DEFAULT_RESPONSE = "MockLLM default response. Add scenarios/default.yaml rules to customize this."


def load_scenarios(path: str = "scenarios/default.yaml") -> List[Scenario]:
    scenario_path = Path(path)
    if not scenario_path.exists():
        return []
    data = yaml.safe_load(scenario_path.read_text()) or []
    if not isinstance(data, list):
        raise ValueError("Scenario file must contain a YAML list.")
    return [Scenario(**item) for item in data]


def normalize_prompt(text: str) -> str:
    return " ".join(text.lower().split())


def find_matching_scenario(prompt: str, scenarios: List[Scenario]) -> Optional[Scenario]:
    normalized = normalize_prompt(prompt)
    for scenario in scenarios:
        match = scenario.match
        if match.exact and normalized == normalize_prompt(match.exact):
            return scenario
        if match.contains and normalize_prompt(match.contains) in normalized:
            return scenario
        if match.regex and re.search(match.regex, prompt, flags=re.IGNORECASE):
            return scenario
    return None


def messages_to_prompt(messages) -> str:
    return "\n".join([m.content for m in messages if m.content])
