# Contributing to deterministic-ai-testing

Thanks for your interest in contributing.

This project exists to help developers build deterministic, reproducible AI testing workflows for modern LLM applications.

## Development setup

#Clone the repository:
git clone https://github.com/relentlessreed/deterministic-ai-testing.git
cd deterministic-ai-testing

# Create and activate a virtual environment:
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies:
pip install -rC

# Run the server:
python3 -m uvicorn app.main:app --reload --port 8000

# Run tests:
pytest

# Contribution guidelines
Please:

- keep pull requests focused and minimal
- include tests when possible
- preserve deterministic behavior
- avoid introducing nondeterministic defaults
- document new features clearly

# Before submitting a PR:
pytest
mockllm snapshot test snapshots/

# Licensing and contribution terms
By submitting a contribution, you agree that your contributions may be used, modified, distributed, sublicensed, and commercially licensed as part of the deterministic-ai-testing project.

You also certify that:

- you have the right to submit the contribution
- the contribution is your original work or appropriately licensed
- the contribution does not knowingly violate third-party intellectual property rights

# Community standards

Be respectful.

Constructive feedback, collaboration, and developer empathy matter more than perfection.

---

# DISCLAIMER LANGUAGE

## README disclaimer section

## Disclaimer

This project is an independent open-source testing framework and is not affiliated with, endorsed by, or sponsored by OpenAI.

OpenAI, ChatGPT, and related marks are trademarks of their respective owners.

This framework is designed for deterministic testing workflows and local AI infrastructure simulation.
