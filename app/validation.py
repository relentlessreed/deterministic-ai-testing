from pathlib import Path

import yaml


class ScenarioValidationError(Exception):
    pass


def validate_scenario(scenario: dict, index: int):
    if not isinstance(scenario, dict):
        raise ScenarioValidationError(
            f"Scenario #{index} must be a dictionary"
        )

    if "match" not in scenario:
        raise ScenarioValidationError(
            f"Scenario #{index} missing required field: 'match'"
        )

    has_response = "response" in scenario
    has_error = "error" in scenario

    if not has_response and not has_error:
        raise ScenarioValidationError(
            f"Scenario #{index} must include either 'response' or 'error'"
        )

    if has_response and has_error:
        raise ScenarioValidationError(
            f"Scenario #{index} cannot include both 'response' and 'error'"
        )

    if not isinstance(scenario["match"], dict):
        raise ScenarioValidationError(
            f"Scenario #{index} field 'match' must be a dictionary"
        )

    if has_response and not isinstance(scenario["response"], dict):
        raise ScenarioValidationError(
            f"Scenario #{index} field 'response' must be a dictionary"
        )

    if has_error and not isinstance(scenario["error"], dict):
        raise ScenarioValidationError(
            f"Scenario #{index} field 'error' must be a dictionary"
        )


def validate_scenarios_file(path: str):
    file_path = Path(path)

    data = yaml.safe_load(file_path.read_text())

    if not isinstance(data, list):
        raise ScenarioValidationError(
            "Scenario file must contain a list of scenarios"
        )

    for index, scenario in enumerate(data, start=1):
        validate_scenario(scenario, index)

    return data
