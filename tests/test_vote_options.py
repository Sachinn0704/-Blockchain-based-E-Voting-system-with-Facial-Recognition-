import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "give_vote.py"
spec = importlib.util.spec_from_file_location("give_vote", MODULE_PATH)
give_vote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(give_vote)


def test_configured_vote_keys_return_expected_choices():
    assert give_vote.get_vote_choice(ord("1")) == "BJP"
    assert give_vote.get_vote_choice(ord("2")) == "CONGRESS"
    assert give_vote.get_vote_choice(ord("3")) == "AAP"
    assert give_vote.get_vote_choice(ord("4")) == "NOTA"


def test_unconfigured_key_does_not_create_a_vote():
    assert give_vote.get_vote_choice(ord("5")) is None
    assert give_vote.get_vote_choice(ord("q")) is None
