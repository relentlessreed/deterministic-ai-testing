from pathlib import Path


def init_project(args):
    scenarios_dir = Path("scenarios")
    snapshots_dir = Path("snapshots")
    tests_dir = Path("tests")

    scenarios_dir.mkdir(exist_ok=True)
    snapshots_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)

    scenario_file = scenarios_dir / "default.yaml"

    if not scenario_file.exists():
        scenario_file.write_text(
            """scenarios:
  - name: hello
    match:
      contains: hello
    response:
      content: Hello from mockllm.
"""
        )

    test_file = tests_dir / "test_ai.py"

    if not test_file.exists():
        test_file.write_text(
            """def test_mockllm():
    assert True
"""
        )

    print("initialized mockllm project")
    print("created:")
    print("  scenarios/default.yaml")
    print("  snapshots/")
    print("  tests/test_ai.py")
