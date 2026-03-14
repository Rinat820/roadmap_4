import pytest
from src.logic.match_logic import MatchManager
from src.exceptions import PlayerNotParticipantError, MatchNotFoundError
from src.dao.dto import PlayerDTO

@pytest.fixture
def match():
    MatchManager.matches = {}
    p1 = PlayerDTO(id=1, name="Privet")
    p2 = PlayerDTO(id=2, name="Poka")
    uuid = "test-uuid"
    MatchManager.create_match(uuid, p1, p2)
    return uuid


def test_win_game_from_40_0(match):
    score = MatchManager.matches[match]["score"]
    score["points"] = [3, 0]
    
    MatchManager.add_point(match, 1)
    
    assert score["games"] == [1, 0]
    assert score["points"] == [0, 0]
    
    
def test_tiebreak_at_6_6(match):
    score = MatchManager.matches[match]["score"]
    score["games"] = [6, 6]
    
    for _ in range(4):
        MatchManager.add_point(match, 1)
        
    assert score["games"] == [6, 6]
    assert score["points"] == [4, 0]


def test_deuce_not_finishing_game(match):
    score = MatchManager.matches[match]["score"]
    score["points"] = [3, 3]

    MatchManager.add_point(match, 1)

    assert score["games"] == [0, 0]
    assert score["points"] == [4, 3]


def test_match_finish_after_two_sets(match):
    score = MatchManager.matches[match]["score"]
    score["sets"] = [1, 0]
    score["games"] = [5, 0]
    score["points"] = [3, 0]
    
    is_finished, updated_match = MatchManager.add_point(match, 1)

    assert is_finished is True
    assert updated_match["winner_id"] == 1 


def test_tiebreak_win_conditions(match):
    """Проверка окончания таймбрейка"""
    score = MatchManager.matches[match]["score"]
    score["games"] = [6, 6]
    score["points"] = [6, 5] 
    
    MatchManager.add_point(match, 1) 
    assert score["sets"] == [1, 0]
    assert score["games"] == [0, 0]
    
    
def test_advantage_back_to_deuce(match):
    """Качели"""
    score = MatchManager.matches[match]["score"]
    score["points"] = [4, 3]
    
    MatchManager.add_point(match, 2)
    assert score["games"] == [0, 0]
    assert score["points"] == [4, 4]

    
def test_add_point_match_not_found():
    fake_uuid = "ne-nastoyachiy-id"
    
    with pytest.raises(MatchNotFoundError):
        MatchManager.add_point(fake_uuid, 1)
        
        
def test_add_point_player_not_participant(match):
    with pytest.raises(PlayerNotParticipantError):
        MatchManager.add_point(match, 999)
