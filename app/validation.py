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
    has_response_sequence = "response_sequence" in scenario

    behavior_count = sum([
        has_response,
        has_error,
        has_response_sequence,
    ])

    if behavior_count == 0:
        raise ScenarioValidationError(
            f"Scenario #{index} must include either 'response', 'error', or 'response_sequence'"
        )

    if behavior_count > 1:
        raise ScenarioValidationError(
            f"Scenario #{index} cannot combine 'response', 'error', and 'response_sequence'"
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


    if has_response_sequence:
        sequence = scenario["response_sequence"]

        if not isinstance(sequence, list):
            raise ScenarioValidationError(
                f"Scenario #{index} field 'response_sequence' must be a list"
            )

        if not sequence:
            raise ScenarioValidationError(
                f"Scenario #{index} field 'response_sequence' cannot be empty"
            )

        for step_index, step in enumerate(sequence, start=1):
            if not isinstance(step, dict):
                raise ScenarioValidationError(
                    f"Scenario #{index} response_sequence step #{step_index} must be a dictionary"
                )

            has_step_response = "response" in step
            has_step_error = "error" in step

            if has_step_response == has_step_error:
                raise ScenarioValidationError(
                    f"Scenario #{index} response_sequence step #{step_index} must include exactly one of 'response' or 'error'"
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
