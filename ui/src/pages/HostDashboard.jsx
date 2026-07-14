import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "../services/api";

const HIDDEN = "████████████████";

export default function HostDashboard() {
    const [board, setBoard] = useState(null);
    const [contestants, setContestants] = useState([]);
    const [gameStatus, setGameStatus] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");

    const refreshStatus = useCallback(async () => {
        try {
            const status = await api.familyFeud.status();

            setGameStatus(status);
            setErrorMessage("");

            if (status.board_loaded) {
                const currentBoard = await api.familyFeud.current();
                setBoard(currentBoard);
            }
        } catch (error) {
            console.error(error);
            setErrorMessage(error.message || "Unable to refresh game status.");
        }
    }, []);

    const refreshContestants = useCallback(async () => {
        try {
            const list = await api.contestants.list();
            setContestants(Array.isArray(list) ? list : []);
        } catch (error) {
            console.error(error);
            setContestants([]);
            setErrorMessage(error.message || "Unable to load contestants.");
        }
    }, []);

    const loadBoard = useCallback(
        async (loader) => {
            try {
                const data = await loader();

                setBoard(data);
                setErrorMessage("");

                await refreshStatus();
            } catch (error) {
                console.error(error);
                setErrorMessage(error.message || "Unable to load board.");
            }
        },
        [refreshStatus]
    );

    useEffect(() => {
        refreshContestants();
        loadBoard(api.familyFeud.nextBoard);
    }, [loadBoard, refreshContestants]);

    useEffect(() => {
        const statusTimer = window.setInterval(refreshStatus, 1000);
        const contestantTimer = window.setInterval(
            refreshContestants,
            5000
        );

        return () => {
            window.clearInterval(statusTimer);
            window.clearInterval(contestantTimer);
        };
    }, [refreshContestants, refreshStatus]);

    const leaderboard = useMemo(
        () =>
            [...contestants].sort(
                (first, second) => second.score - first.score
            ),
        [contestants]
    );

    const timer = useMemo(() => {
        const seconds = gameStatus?.timer_seconds ?? 0;
        const minutes = String(Math.floor(seconds / 60)).padStart(
            2,
            "0"
        );
        const remainingSeconds = String(seconds % 60).padStart(
            2,
            "0"
        );

        return `${minutes}:${remainingSeconds}`;
    }, [gameStatus]);

    async function openRound() {
        try {
            await api.familyFeud.openRound();
            await refreshStatus();
        } catch (error) {
            console.error(error);
            setErrorMessage(error.message || "Unable to open round.");
        }
    }

    async function closeRound() {
        try {
            await api.familyFeud.closeRound();
            await refreshStatus();
        } catch (error) {
            console.error(error);
            setErrorMessage(error.message || "Unable to close round.");
        }
    }

    async function resetRound() {
        try {
            const updatedBoard = await api.familyFeud.resetRound();

            if (updatedBoard?.answers) {
                setBoard(updatedBoard);
            }

            await refreshStatus();
        } catch (error) {
            console.error(error);
            setErrorMessage(error.message || "Unable to reset round.");
        }
    }

    async function revealRemaining() {
        try {
            const updatedBoard =
                await api.familyFeud.revealRemaining();

            setBoard(updatedBoard);
            await refreshStatus();
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to reveal remaining answers."
            );
        }
    }

    // Individual Answer Reveal
    async function revealAnswer(rank) {
        try {
            const updatedBoard = await api.familyFeud.revealAnswer(
                rank
            );

            setBoard(updatedBoard);
            await refreshStatus();
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to reveal answer."
            );
        }
    }

    return (
        <div className="dashboard">
            <header className="topbar">
                <div>
                    <h1>TikTrivia Pro</h1>
                    <p>Professional Host Dashboard</p>
                </div>

                <div className="live">
                    {gameStatus?.question_open
                        ? "🟢 LIVE"
                        : "⚪ CLOSED"}
                </div>
            </header>

            <div className="main-grid">
                <section className="left-panel">
                    <h2>Contestants</h2>

                    <div className="contestant-mode">
                        Registration Mode
                        <br />
                        <b>Hybrid</b>
                    </div>

                    <hr />

                    {leaderboard.length === 0 ? (
                        <div className="placeholder">
                            No contestants
                        </div>
                    ) : (
                        leaderboard.map((player) => (
                            <div
                                className="contestant-row"
                                key={player.id}
                            >
                                <span>{player.display_name}</span>
                                <b>{player.score}</b>
                            </div>
                        ))
                    )}
                </section>

                <section className="center-panel">
                    {errorMessage && (
                        <div className="error-message">
                            {errorMessage}
                        </div>
                    )}

                    <div className="board-header">
                        <div>
                            <b>{board?.board_id || "No Board"}</b>
                        </div>

                        <div>{board?.category || "—"}</div>
                    </div>

                    <div className="question">
                        {board?.survey_question ||
                            "Load a board to begin."}
                    </div>

                    {board?.answers?.map((answer) => (
                        <div className="answer" key={answer.id}>
                            <div className="rank">{answer.rank}</div>

                            <div className="answer-text">
                                {answer.revealed ? answer.answer : HIDDEN}
                            </div>

                            <div>
                                {answer.revealed ? answer.points : ""}
                            </div>

                            {/* Individual Answer Reveal */}
                            <div className="answer-controls">
                                <button
                                    type="button"
                                    onClick={() =>
                                        revealAnswer(answer.rank)
                                    }
                                    disabled={answer.revealed === true}
                                >
                                    {answer.revealed
                                        ? "Revealed"
                                        : "Reveal"}
                                </button>
                            </div>
                        </div>
                    ))}

                    <div className="status-bar">
                        <div>
                            Round
                            <br />
                            <b>
                                {gameStatus?.question_open
                                    ? "OPEN"
                                    : "CLOSED"}
                            </b>
                        </div>

                        <div>
                            Answers
                            <br />
                            <b>
                                {gameStatus?.answers_found?.length ??
                                    0}
                                {" / "}
                                {board?.answers?.length ?? 0}
                            </b>
                        </div>

                        <div>
                            Remaining
                            <br />
                            <b>
                                {gameStatus?.remaining_answers ?? 0}
                            </b>
                        </div>

                        <div>
                            Timer
                            <br />
                            <b>{timer}</b>
                        </div>
                    </div>
                </section>

                <section className="right-panel">
                    <h2>Host Command Center</h2>

                    <button
                        type="button"
                        onClick={openRound}
                        disabled={
                            !board ||
                            gameStatus?.question_open === true
                        }
                    >
                        ▶ Open Round
                    </button>

                    <button
                        type="button"
                        onClick={closeRound}
                        disabled={
                            !board ||
                            gameStatus?.question_open !== true
                        }
                    >
                        ■ Close Round
                    </button>

                    <button
                        type="button"
                        onClick={() =>
                            loadBoard(
                                api.familyFeud.previousBoard
                            )
                        }
                    >
                        ⏮ Previous Board
                    </button>

                    <button
                        type="button"
                        onClick={() =>
                            loadBoard(api.familyFeud.nextBoard)
                        }
                    >
                        ⏭ Next Board
                    </button>

                    <button
                        type="button"
                        onClick={revealRemaining}
                        disabled={!board}
                    >
                        👁 Reveal Remaining
                    </button>

                    <button
                        type="button"
                        onClick={resetRound}
                        disabled={!board}
                    >
                        🔄 Reset Round
                    </button>

                    <hr />

                    <h3>Live Event Log</h3>

                    <div className="event-log">
                        {gameStatus?.event_log?.length ? (
                            gameStatus.event_log.map(
                                (event, index) => (
                                    <div key={`${event}-${index}`}>
                                        {event}
                                    </div>
                                )
                            )
                        ) : (
                            <div>No events.</div>
                        )}
                    </div>
                </section>
            </div>
        </div>
    );
}
