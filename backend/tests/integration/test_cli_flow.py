import pytest
from unittest.mock import patch
from src.main import main

# Mock inputs for the Menu flow:
# 1 -> Description (Add)
# 2 (List)
# 7 (Exit)
@patch('builtins.input', side_effect=['1', 'Buy milk', '2', '7'])
def test_add_list_flow(mock_input, capsys):
    try:
        main()
    except SystemExit:
        pass
    
    captured = capsys.readouterr()
    assert "Task 1 added" in captured.out
    assert "Buy milk" in captured.out

# 1 -> Buy milk
# 5 -> 1 (Complete)
# 2 (List)
# 7 (Exit)
@patch('builtins.input', side_effect=['1', 'Buy milk', '5', '1', '2', '7'])
def test_complete_flow(mock_input, capsys):
    try:
        main()
    except SystemExit:
        pass
    
    captured = capsys.readouterr()
    assert "[x] 1: Buy milk" in captured.out

# 1 -> Buy milk
# 3 -> 1 -> Buy almond milk (Update)
# 4 -> 1 (Delete)
# 2 (List)
# 7 (Exit)
@patch('builtins.input', side_effect=['1', 'Buy milk', '3', '1', 'Buy almond milk', '4', '1', '2', '7'])
def test_update_delete_flow(mock_input, capsys):
    try:
        main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "Task 1 updated" in captured.out
    assert "Task 1 deleted" in captured.out