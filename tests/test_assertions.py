import pytest

from mockllm.assertions import assert_tool_called, assert_tool_called_with


def tool_response():
    return {
        "choices": [
            {
                "message": {
                    "tool_calls": [
                        {
                            "id": "call_mock_1",
                            "type": "function",
                            "function": {
                                "name": "search_docs",
                                "arguments": "{\"query\":\"refund policy\"}",
                            },
                        }
                    ]
                }
            }
        ]
    }


def test_assert_tool_called_passes():
    assert_tool_called(tool_response(), "search_docs")


def test_assert_tool_called_with_passes():
    assert_tool_called_with(
        tool_response(),
        "search_docs",
        {"query": "refund policy"},
    )


def test_assert_tool_called_fails():
    with pytest.raises(AssertionError):
        assert_tool_called(tool_response(), "missing_tool")


def test_assert_tool_called_with_fails_on_argument():
    with pytest.raises(AssertionError):
        assert_tool_called_with(
            tool_response(),
            "search_docs",
            {"query": "wrong"},
        )
