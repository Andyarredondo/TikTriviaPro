"""
==========================================================
TikTrivia Pro
Game State Manager
Version 0.5.0
==========================================================
"""

from __future__ import annotations

from datetime import datetime


class GameState:
    """
    Stores the current live game entirely in memory.

    This object is the single source of truth for the active
    board, round state, revealed answers, timer, and event log.
    """

    def __init__(self):
        self.event_log: list[str] = []
        self.reset()

    # -----------------------------------------------------
    # Event Log
    # -----------------------------------------------------

    def add_event(
        self,
        message: str,
    ) -> None:
        """
        Add a timestamped entry to the live event log.
        """

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.event_log.insert(
            0,
            f"{timestamp}  {message}",
        )

        self.event_log = self.event_log[:100]

    # -----------------------------------------------------
    # Reset Entire Game
    # -----------------------------------------------------

    def reset(self) -> None:
        """
        Clear the active game and reset all live state.
        """

        self.board = None
        self.running = False
        self.question_open = False
        self.registration_mode = "Hybrid"
        self.timer_seconds = 0
        self.question_number = 0
        self.answers_found: list[int] = []
        self.correct_players: dict[int, str] = {}
        self.score_history: dict[int, list[int]] = {}
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.board_source: str = "Entire Database"
        self.random_deck_ids: list[str] = []
        self.random_deck_position: int = 0
        self.random_deck_last_played: list[str] = []
        self.random_deck_auto_reshuffle: bool = False
        self.selected_category: str | None = None
        self.viewer_overlay_state: str = "BOARD"

        self.event_log.clear()
        self.add_event("Game reset.")

    # -----------------------------------------------------
    # Random Deck
    # -----------------------------------------------------

    def record_random_deck_played(self, board_id: str | None) -> None:
        """
        Track the most recently played board IDs for the random deck.
        """

        if not board_id:
            return

        self.random_deck_last_played = [
            board_id,
            *[entry for entry in self.random_deck_last_played if entry != board_id],
        ][:10]

    def random_deck_status(self) -> dict:
        """
        Return the current random deck status.
        """

        total_boards = len(self.random_deck_ids)
        boards_played = self.random_deck_position
        boards_remaining = max(total_boards - boards_played, 0)

        return {
            "total_boards": total_boards,
            "boards_remaining": boards_remaining,
            "boards_played": boards_played,
            "last_10_boards": list(self.random_deck_last_played),
            "auto_reshuffle": self.random_deck_auto_reshuffle,
        }

    # -----------------------------------------------------
    # Load Board
    # -----------------------------------------------------

    def load_board(self, board) -> None:
        """
        Load a new board and reset round-specific state.
        """

        self.board = board
        self.running = False
        self.question_open = False
        self.timer_seconds = 0
        self.answers_found = []
        self.correct_players = {}
        self.start_time = None
        self.end_time = None
        self.viewer_overlay_state = "STANDBY"

        if board is not None:
            for answer in board.answers:
                answer.revealed = False

        self.add_event(
            f"Board loaded: {getattr(board, 'board_id', 'Unknown')}"
        )

    # -----------------------------------------------------
    # Open Question
    # -----------------------------------------------------

    def open_question(self) -> None:
        """
        Open the round and begin accepting answers.
        """

        self.running = True
        self.question_open = True
        self.start_time = datetime.now()
        self.end_time = None
        self.viewer_overlay_state = "BOARD"

        if self.board is not None:
            for answer in self.board.answers:
                answer.revealed = False

        self.answers_found.clear()

        self.add_event("Round opened.")

    # -----------------------------------------------------
    # Close Question
    # -----------------------------------------------------

    def close_question(self) -> None:
        """
        Close the round and stop accepting answers.
        """

        self.running = False
        self.question_open = False
        self.end_time = datetime.now()
        self.viewer_overlay_state = "STANDBY"

        self.add_event("Round closed.")

    # -----------------------------------------------------
    # Reveal Answer
    # -----------------------------------------------------

    def reveal_answer(
        self,
        rank: int,
    ) -> None:
        """
        Record an answer rank as revealed.
        """

        if rank not in self.answers_found:
            self.answers_found.append(rank)
            self.answers_found.sort()

            self.add_event(
                f"Answer #{rank} revealed."
            )

    # -----------------------------------------------------
    # Already Revealed?
    # -----------------------------------------------------

    def is_revealed(
        self,
        rank: int,
    ) -> bool:
        """
        Return True when an answer rank has been revealed.
        """

        return rank in self.answers_found

    # -----------------------------------------------------
    # Record Player
    # -----------------------------------------------------

    def record_player(
        self,
        rank: int,
        username: str,
    ) -> None:
        """
        Record the player who found a ranked answer.
        """

        self.correct_players[rank] = username

        self.add_event(
            f"{username} found answer #{rank}."
        )
    # -----------------------------------------------------
    # Score History
    # -----------------------------------------------------

    def record_score_change(
        self,
        contestant_id: int,
        amount: int,
    ) -> None:
        """
        Store one score adjustment for a contestant.
        """

        history = self.score_history.setdefault(
            contestant_id,
            [],
        )

        history.append(amount)

    def pop_last_score_change(
        self,
        contestant_id: int,
    ) -> int | None:
        """
        Remove and return the contestant's most recent score change.
        """

        history = self.score_history.get(
            contestant_id
        )

        if not history:
            return None

        amount = history.pop()

        if not history:
            self.score_history.pop(
                contestant_id,
                None,
            )

        return amount    
    
    # -----------------------------------------------------
    # Remaining Answers
    # -----------------------------------------------------

    def remaining_answers(self) -> int:
        """
        Return the number of unrevealed answers.
        """

        if self.board is None:
            return 0

        try:
            total = len(self.board.answers)
        except Exception:
            return 0

        return max(
            total - len(self.answers_found),
            0,
        )

    # -----------------------------------------------------
    # Board Complete?
    # -----------------------------------------------------

    def board_complete(self) -> bool:
        """
        Return True when all answers have been revealed.
        """

        return (
            self.board is not None
            and self.remaining_answers() == 0
        )

    # -----------------------------------------------------
    # Timer
    # -----------------------------------------------------

    def update_timer(self) -> int:
        """
        Update and return elapsed round time in seconds.
        """

        if self.question_open and self.start_time is not None:
            elapsed = datetime.now() - self.start_time
            self.timer_seconds = int(elapsed.total_seconds())

        return self.timer_seconds

    # -----------------------------------------------------
    # Status
    # -----------------------------------------------------

    def status(self) -> dict:
        """
        Return the complete live game state.
        """

        self.update_timer()

        return {
            "running": self.running,
            "question_open": self.question_open,
            "board_loaded": self.board is not None,
            "board_id": getattr(
                self.board,
                "board_id",
                None,
            ),
            "category": getattr(
                self.board,
                "category",
                None,
            ),
            "survey_question": getattr(
                self.board,
                "survey_question",
                None,
            ),
            "registration_mode": self.registration_mode,
            "answers_found": list(self.answers_found),
            "correct_players": dict(self.correct_players),
            "remaining_answers": self.remaining_answers(),
            "timer_seconds": self.timer_seconds,
            "event_log": list(self.event_log),
            "viewer_overlay_state": self.viewer_overlay_state,
        }


GAME = GameState()