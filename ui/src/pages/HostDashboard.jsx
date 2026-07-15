import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "../services/api";
import ProductionManager from "../components/ProductionManager";

const HIDDEN = "████████████████";

export default function HostDashboard() {
    const [board, setBoard] = useState(null);
    const [contestants, setContestants] = useState([]);
    const [gameStatus, setGameStatus] = useState(null);
    const [randomDeck, setRandomDeck] = useState(null);
    const [boardSource, setBoardSource] = useState("Entire Database");
    const [selectedCategory, setSelectedCategory] = useState("");
    const [selectedAnswerRank, setSelectedAnswerRank] = useState("");
    const [productionPlayback, setProductionPlayback] = useState(null);
    const [playbackBusy, setPlaybackBusy] = useState(false);
    const [categories, setCategories] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");
    const [selectedProduction, setSelectedProduction] = useState(null);

    const refreshStatus = useCallback(async () => {
        try {
            const [status, deckStatus] = await Promise.all([
                api.familyFeud.status(),
                api.familyFeud.randomDeckStatus(),
            ]);

            setGameStatus(status);
            setRandomDeck(deckStatus);
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
        const initializeDashboard = async () => {
            try {
                const [source, categoryList] = await Promise.all([
                    api.familyFeud.getBoardSource(),
                    api.familyFeud.getCategories(),
                ]);

                setBoardSource(source?.board_source || "Entire Database");
                setCategories(categoryList?.categories || []);

                if (source?.board_source === "Category") {
                    const nextCategory = source?.selected_category || categoryList?.categories?.[0] || "";
                    setSelectedCategory(nextCategory);
                } else {
                    setSelectedCategory("");
                }
            } catch (error) {
                console.error(error);
            }

            refreshContestants();
            await refreshProductionPlaybackCurrent();
            loadBoard(api.familyFeud.nextBoard);
        };

        initializeDashboard();
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

    const boardAnswers = board?.answers || [];

    useEffect(() => {
        const nextSelectedRank =
            boardAnswers.find((answer) => !answer.revealed)?.rank ??
            boardAnswers[0]?.rank ??
            "";

        setSelectedAnswerRank(
            nextSelectedRank === null || nextSelectedRank === undefined
                ? ""
                : String(nextSelectedRank)
        );
    }, [boardAnswers]);

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

    const boardLocked =
        gameStatus?.board_loaded === true &&
        gameStatus?.question_open === true;

    const isRandomDeckComplete =
        (randomDeck?.total_boards ?? 0) > 0 &&
        (randomDeck?.boards_remaining ?? 0) === 0;

    const isProductionSource = boardSource === "Production";
    const hasActiveProductionPlayback = Boolean(
        productionPlayback?.production_id
    );

    const playbackProductionName =
        productionPlayback?.production_name || "No active production";

    const playbackCurrentItem = productionPlayback?.current_item || null;

    const playbackProgressText =
        productionPlayback?.item_count != null
            ? `${productionPlayback.current_index + 1} / ${productionPlayback.item_count}`
            : "-";

    const playbackEngineText = playbackCurrentItem?.engine
        ? playbackCurrentItem.engine
              .split("_")
              .map((segment) =>
                  segment
                      ? segment.charAt(0).toUpperCase() + segment.slice(1)
                      : segment
              )
              .join(" ")
        : "-";

    const playbackItemIdText = playbackCurrentItem?.item_id || "-";

    async function refreshProductionPlaybackCurrent({
        suppressError = true,
    } = {}) {
        try {
            const current = await api.productionPlayback.current();
            setProductionPlayback(current);
        } catch (error) {
            setProductionPlayback(null);

            if (!suppressError) {
                console.error(error);
                setErrorMessage(
                    error.message || "Unable to load production playback."
                );
            }
        }
    }

    async function startProductionPlayback() {
        if (!selectedProduction?.id) {
            setErrorMessage("Select a production to start.");
            return;
        }

        setPlaybackBusy(true);

        try {
            const playback = await api.productionPlayback.start(
                selectedProduction?.id
            );

            setProductionPlayback(playback);
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to start production playback."
            );
        } finally {
            setPlaybackBusy(false);
        }
    }

    async function nextProductionPlaybackItem() {
        setPlaybackBusy(true);

        try {
            const playback = await api.productionPlayback.next();
            setProductionPlayback(playback);
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to advance production playback."
            );
        } finally {
            setPlaybackBusy(false);
        }
    }

    async function previousProductionPlaybackItem() {
        setPlaybackBusy(true);

        try {
            const playback = await api.productionPlayback.previous();
            setProductionPlayback(playback);
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to move production playback back."
            );
        } finally {
            setPlaybackBusy(false);
        }
    }

    async function endProductionPlayback() {
        setPlaybackBusy(true);

        try {
            await api.productionPlayback.end();
            setProductionPlayback(null);
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to end production playback."
            );
        } finally {
            setPlaybackBusy(false);
        }
    }

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

    async function revealNextAnswer() {
        const nextAnswer = boardAnswers.find((answer) => !answer.revealed);

        if (!nextAnswer) {
            setErrorMessage("All answers are already revealed.");
            return;
        }

        await revealAnswer(nextAnswer.rank);
    }

    async function revealSelectedAnswer() {
        if (!selectedAnswerRank) {
            setErrorMessage("Select an answer to reveal.");
            return;
        }

        await revealAnswer(Number(selectedAnswerRank));
    }

    async function resetAllScores() {
        try {
            await Promise.all(
                contestants.map((player) => api.contestants.resetScore(player.id))
            );

            await refreshContestants();
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(error.message || "Unable to reset scores.");
        }
    }

    async function nextRandomBoard() {
        try {
            const updatedBoard = await api.familyFeud.randomDeckNext();

            if (updatedBoard?.answers) {
                setBoard(updatedBoard);
            }

            await refreshStatus();
            setErrorMessage("");
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to load the next random board."
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
                    <h2>Live Players</h2>

                    <div className="contestant-mode">
                        Registration Mode
                        <br />
                        <select
                            value={
                                gameStatus?.registration_mode || "Hybrid"
                            }
                            onChange={async (event) => {
                                const nextMode = event.target.value;

                                try {
                                    const updatedStatus = await api.familyFeud.setRegistrationMode(
                                        nextMode
                                    );

                                    setGameStatus(updatedStatus);
                                    setErrorMessage("");
                                } catch (error) {
                                    console.error(error);
                                    setErrorMessage(
                                        error.message ||
                                            "Unable to update registration mode."
                                    );
                                }
                            }}
                        >
                            <option value="Auto">Auto</option>
                            <option value="Manual">Manual</option>
                            <option value="Hybrid">Hybrid</option>
                        </select>
                    </div>

                    <div className="player-header-row">
                        <span>Player Name</span>
                        <span>Current Score</span>
                    </div>

                    {leaderboard.length === 0 ? (
                        <div className="placeholder">
                            No live players
                        </div>
                    ) : (
                        leaderboard.map((player) => (
                            <div
                                className="contestant-row live-player-row"
                                key={player.id}
                            >
                                <span className="live-player-name">{player.display_name}</span>
                                <b className="live-player-points">{player.score}</b>
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

                    <div className="console-grid">
                        <div className="deck-card console-card console-card--wide">
                            <h3>Production</h3>

                            <div className="deck-history">
                                <span>Selected Production</span>
                                <strong>
                                    {selectedProduction?.production_name || "None Selected"}
                                </strong>
                            </div>

                            <div className="board-control-row">
                                <button
                                    type="button"
                                    onClick={startProductionPlayback}
                                    disabled={playbackBusy || !selectedProduction?.id}
                                >
                                    <span className="button-icon">▶</span>
                                    <span className="button-label">
                                        <span>Start</span>
                                        <span>Production</span>
                                    </span>
                                </button>
                            </div>

                            <div className="board-control-row console-button-grid console-button-grid--three">
                                <button
                                    type="button"
                                    onClick={previousProductionPlaybackItem}
                                    disabled={playbackBusy || !hasActiveProductionPlayback}
                                    title={
                                        !hasActiveProductionPlayback
                                            ? "Start production playback first."
                                            : undefined
                                    }
                                >
                                    <span className="button-icon">◀</span>
                                    <span className="button-label">
                                        <span>Previous</span>
                                        <span>Production Item</span>
                                    </span>
                                </button>

                                <button
                                    type="button"
                                    onClick={nextProductionPlaybackItem}
                                    disabled={playbackBusy || !hasActiveProductionPlayback}
                                    title={
                                        !hasActiveProductionPlayback
                                            ? "Start production playback first."
                                            : undefined
                                    }
                                >
                                    <span className="button-icon">▶</span>
                                    <span className="button-label">
                                        <span>Next</span>
                                        <span>Production Item</span>
                                    </span>
                                </button>

                                <button
                                    type="button"
                                    onClick={endProductionPlayback}
                                    disabled={playbackBusy || !hasActiveProductionPlayback}
                                    title={
                                        !hasActiveProductionPlayback
                                            ? "Start production playback first."
                                            : undefined
                                    }
                                >
                                    <span className="button-icon">⏹</span>
                                    <span className="button-label">
                                        <span>End</span>
                                        <span>Production</span>
                                    </span>
                                </button>
                            </div>

                            <div className="deck-stats">
                                <div>
                                    <span>Current Production</span>
                                    <strong>{playbackProductionName}</strong>
                                </div>

                                <div>
                                    <span>Current Item</span>
                                    <strong>{playbackCurrentItem?.sequence ?? "-"}</strong>
                                </div>
                            </div>

                            <div className="deck-history">
                                <span>Progress</span>
                                <strong>{playbackProgressText}</strong>
                            </div>

                            <div className="deck-stats">
                                <div>
                                    <span>Current Engine</span>
                                    <strong>{playbackEngineText}</strong>
                                </div>

                                <div>
                                    <span>Current Item ID</span>
                                    <strong>{playbackItemIdText}</strong>
                                </div>
                            </div>

                            <ProductionManager
                                selectedProduction={selectedProduction}
                                setSelectedProduction={setSelectedProduction}
                            />
                        </div>

                        <div className="deck-card console-card console-card--wide">
                            <h3>Game Controls</h3>

                            <div className="board-control-group">
                                <div className="board-control-label">Round Control</div>
                                <div className="board-control-row">
                                    <button
                                        type="button"
                                        onClick={openRound}
                                        disabled={
                                            !board ||
                                            gameStatus?.question_open === true
                                        }
                                    >
                                        <span className="button-icon">▶</span>
                                        <span className="button-label">
                                            <span>Open</span>
                                            <span>Round</span>
                                        </span>
                                    </button>

                                    <button
                                        type="button"
                                        onClick={closeRound}
                                        disabled={
                                            !board ||
                                            gameStatus?.question_open !== true
                                        }
                                    >
                                        <span className="button-icon">■</span>
                                        <span className="button-label">
                                            <span>Close</span>
                                            <span>Round</span>
                                        </span>
                                    </button>
                                </div>
                            </div>

                            <div className="board-control-group">
                                <div className="board-control-label">Board Source</div>
                                <div className="board-control-row">
                                    <select
                                        value={boardSource}
                                        onChange={async (event) => {
                                            const nextSource = event.target.value;

                                            if (nextSource === "Production") {
                                                setBoardSource(nextSource);
                                                setSelectedCategory("");
                                                await refreshProductionPlaybackCurrent();
                                                setErrorMessage("");
                                                return;
                                            }

                                            if (nextSource === "Random Deck") {
                                                setBoardSource(nextSource);
                                                setSelectedCategory("");
                                                setErrorMessage("");
                                                return;
                                            }

                                            try {
                                                const updatedSource = await api.familyFeud.setBoardSource(nextSource);
                                                setBoardSource(updatedSource?.board_source || nextSource);
                                                setSelectedCategory(updatedSource?.selected_category || "");
                                                if (updatedSource?.board) {
                                                    setBoard(updatedSource.board);
                                                }
                                                if (updatedSource?.deck_status) {
                                                    setRandomDeck(updatedSource.deck_status);
                                                }
                                                setErrorMessage("");
                                            } catch (error) {
                                                console.error(error);
                                                setErrorMessage(
                                                    error.message ||
                                                        "Unable to update board source."
                                                );
                                            }
                                        }}
                                    >
                                        <option value="Entire Database">Entire Database</option>
                                        <option value="Category">Category</option>
                                        <option value="Production">Production</option>
                                        <option value="Random Deck">Random Deck</option>
                                    </select>
                                </div>
                            </div>

                            <div className="board-control-group">
                                <div className="board-control-label">Board Navigation</div>
                                <div className="board-control-row">
                                    <button
                                        type="button"
                                        onClick={() => loadBoard(api.familyFeud.firstBoard)}
                                        disabled={boardLocked || isProductionSource}
                                        title={
                                            boardLocked
                                                ? "Close the current board before changing boards."
                                                : isProductionSource
                                                    ? "Use Production controls while Production is selected."
                                                    : undefined
                                        }
                                    >
                                        <span className="button-icon">⏮</span>
                                        <span className="button-label">
                                            <span>First</span>
                                            <span>Board</span>
                                        </span>
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() => loadBoard(api.familyFeud.previousBoard)}
                                        disabled={boardLocked || isProductionSource}
                                        title={
                                            boardLocked
                                                ? "Close the current board before changing boards."
                                                : isProductionSource
                                                    ? "Use Production controls while Production is selected."
                                                    : undefined
                                        }
                                    >
                                        <span className="button-icon">◀</span>
                                        <span className="button-label">
                                            <span>Previous</span>
                                            <span>Board</span>
                                        </span>
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() => loadBoard(api.familyFeud.nextBoard)}
                                        disabled={boardLocked || isProductionSource}
                                        title={
                                            boardLocked
                                                ? "Close the current board before changing boards."
                                                : isProductionSource
                                                    ? "Use Production controls while Production is selected."
                                                    : undefined
                                        }
                                    >
                                        <span className="button-icon">▶</span>
                                        <span className="button-label">
                                            <span>Next</span>
                                            <span>Board</span>
                                        </span>
                                    </button>
                                </div>
                            </div>

                            {boardSource === "Category" && (
                                <div className="board-control-group">
                                    <div className="board-control-label">Category</div>
                                    <div className="board-control-row">
                                        <select
                                            value={selectedCategory}
                                            onChange={async (event) => {
                                                const nextCategory = event.target.value;

                                                try {
                                                    const updatedSource = await api.familyFeud.setCategorySource(nextCategory);
                                                    setBoardSource(updatedSource?.board_source || "Category");
                                                    setSelectedCategory(updatedSource?.selected_category || nextCategory);
                                                    if (updatedSource?.board) {
                                                        setBoard(updatedSource.board);
                                                    }
                                                    if (updatedSource?.deck_status) {
                                                        setRandomDeck(updatedSource.deck_status);
                                                    }
                                                    setErrorMessage("");
                                                } catch (error) {
                                                    console.error(error);
                                                    setErrorMessage(
                                                        error.message ||
                                                            "Unable to update category."
                                                    );
                                                }
                                            }}
                                        >
                                            {categories.length === 0 ? (
                                                <option value="">No categories found</option>
                                            ) : (
                                                categories.map((category) => (
                                                    <option key={category} value={category}>
                                                        {category}
                                                    </option>
                                                ))
                                            )}
                                        </select>
                                    </div>
                                </div>
                            )}

                            <div className="board-control-group">
                                <div className="board-control-label">Board Actions</div>

                                <div className="board-control-row">
                                    <button
                                        type="button"
                                        onClick={revealNextAnswer}
                                        disabled={!board || boardAnswers.every((answer) => answer.revealed)}
                                    >
                                        <span className="button-icon">👁</span>
                                        <span className="button-label">
                                            <span>Reveal Next</span>
                                            <span>Answer</span>
                                        </span>
                                    </button>

                                    <select
                                        value={selectedAnswerRank}
                                        onChange={(event) => setSelectedAnswerRank(event.target.value)}
                                        disabled={!board || boardAnswers.length === 0}
                                    >
                                        <option value="">Reveal specific answer</option>
                                        {boardAnswers.map((answer) => (
                                            <option key={answer.id} value={answer.rank}>
                                                {answer.rank}. {answer.answer}
                                            </option>
                                        ))}
                                    </select>

                                    <button
                                        type="button"
                                        onClick={revealSelectedAnswer}
                                        disabled={!board || !selectedAnswerRank}
                                    >
                                        <span className="button-icon">🎯</span>
                                        <span className="button-label">
                                            <span>Reveal</span>
                                            <span>Specific</span>
                                        </span>
                                    </button>
                                </div>

                                <div className="board-control-row">
                                    <button
                                        type="button"
                                        onClick={revealRemaining}
                                        disabled={!board}
                                    >
                                        <span className="button-icon">✨</span>
                                        <span className="button-label">
                                            <span>Reveal All</span>
                                            <span>Answers</span>
                                        </span>
                                    </button>

                                    {/* TODO: wire hide-all answers backend action. */}
                                    <button type="button" disabled>
                                        <span className="button-icon">🙈</span>
                                        <span className="button-label">
                                            <span>Hide All</span>
                                            <span>Answers</span>
                                        </span>
                                    </button>

                                    {/* TODO: wire blank-board backend action. */}
                                    <button type="button" disabled>
                                        <span className="button-icon">⬛</span>
                                        <span className="button-label">
                                            <span>Blank</span>
                                            <span>Board</span>
                                        </span>
                                    </button>

                                    {/* TODO: wire show-board backend action. */}
                                    <button type="button" disabled>
                                        <span className="button-icon">🖥</span>
                                        <span className="button-label">
                                            <span>Show</span>
                                            <span>Board</span>
                                        </span>
                                    </button>
                                </div>

                                <div className="board-control-row">
                                    <button
                                        type="button"
                                        onClick={resetRound}
                                        disabled={!board}
                                    >
                                        <span className="button-icon">🔄</span>
                                        <span className="button-label">
                                            <span>Reset</span>
                                            <span>Round</span>
                                        </span>
                                    </button>
                                </div>
                            </div>

                            <div className="board-control-row console-button-grid console-button-grid--two">
                                {/* TODO: wire round mode backend action. */}
                                <button type="button" disabled>
                                    <span className="button-icon">◉</span>
                                    <span className="button-label">
                                        <span>Normal</span>
                                        <span>Round</span>
                                    </span>
                                </button>

                                {/* TODO: wire fast money backend action. */}
                                <button type="button" disabled>
                                    <span className="button-icon">⚡</span>
                                    <span className="button-label">
                                        <span>Fast</span>
                                        <span>Money</span>
                                    </span>
                                </button>
                            </div>
                        </div>

                        <div className="deck-card console-card">
                            <h3>Broadcast</h3>

                            <div className="board-control-row console-button-grid console-button-grid--two">
                                {/* TODO: wire intro broadcast action. */}
                                <button type="button" disabled>
                                    <span className="button-icon">✨</span>
                                    <span className="button-label">
                                        <span>Intro</span>
                                    </span>
                                </button>

                                {/* TODO: wire outro broadcast action. */}
                                <button type="button" disabled>
                                    <span className="button-icon">🌙</span>
                                    <span className="button-label">
                                        <span>Outro</span>
                                    </span>
                                </button>

                                {/* TODO: wire commercial break action. */}
                                <button type="button" disabled>
                                    <span className="button-icon">⏸</span>
                                    <span className="button-label">
                                        <span>Commercial</span>
                                        <span>Break</span>
                                    </span>
                                </button>

                                {/* TODO: wire resume-show action. */}
                                <button type="button" disabled>
                                    <span className="button-icon">▶</span>
                                    <span className="button-label">
                                        <span>Resume</span>
                                        <span>Show</span>
                                    </span>
                                </button>
                            </div>
                        </div>

                        <div className="deck-card console-card">
                            <h3>Random Deck</h3>

                            <div className="board-control-row">
                                <button
                                    type="button"
                                    onClick={async () => {
                                        try {
                                            await api.familyFeud.randomDeckNew();
                                            const currentBoard = await api.familyFeud.current();
                                            if (currentBoard?.answers) {
                                                setBoard(currentBoard);
                                            }
                                            await refreshStatus();
                                            setErrorMessage("");
                                        } catch (error) {
                                            console.error(error);
                                            setErrorMessage(
                                                error.message ||
                                                    "Unable to create a new random deck."
                                            );
                                        }
                                    }}
                                    disabled={boardLocked}
                                    title={
                                        boardLocked
                                            ? "Close the current board before changing boards."
                                            : undefined
                                    }
                                >
                                    <span className="button-icon">🔀</span>
                                    <span className="button-label">
                                        <span>New Random</span>
                                        <span>Deck</span>
                                    </span>
                                </button>

                                <button
                                    type="button"
                                    onClick={nextRandomBoard}
                                    disabled={boardLocked || isRandomDeckComplete}
                                    title={
                                        boardLocked
                                            ? "Close the current board before changing boards."
                                            : isRandomDeckComplete
                                                ? "The current random deck is complete."
                                                : undefined
                                    }
                                >
                                    <span className="button-icon">🎲</span>
                                    <span className="button-label">
                                        <span>Next</span>
                                        <span>Random</span>
                                    </span>
                                </button>
                            </div>

                            <div className="deck-stats compact-stats">
                                <div>
                                    <span>Boards Remaining</span>
                                    <strong>{randomDeck?.boards_remaining ?? 0}</strong>
                                </div>

                                <div>
                                    <span>Boards Played</span>
                                    <strong>{randomDeck?.boards_played ?? 0}</strong>
                                </div>
                            </div>

                            {isRandomDeckComplete && (
                                <div className="deck-complete-message">
                                    Random Deck complete. Start a new deck to continue.
                                </div>
                            )}

                            <div className="deck-history">
                                <span>Last 10 Boards</span>
                                <ul>
                                    {randomDeck?.last_10_boards?.length ? (
                                        randomDeck.last_10_boards.map(
                                            (boardId) => (
                                                <li key={boardId}>{boardId}</li>
                                            )
                                        )
                                    ) : (
                                        <li>None yet</li>
                                    )}
                                </ul>
                            </div>
                        </div>

                        <div className="deck-card console-card console-card--wide">
                            <h3>Event Log</h3>

                            <div className="event-log compact-event-log">
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
                        </div>

                    </div>
                </section>
            </div>
        </div>
    );
}
