import React, { useMemo } from "react";

import AnswerPlaque from "../AnswerPlaque";

import "../../theme/overlay.css";

export default function FriendlyFeudOverlay({
    board,
    status,
}) {
    const answers = Array.isArray(board?.answers)
        ? board.answers
        : [];

    const hasBoard = Boolean(
        board?.board_id &&
        board?.survey_question
    );

    const timer = useMemo(() => {
        const seconds = status?.timer_seconds ?? 0;
        const m = String(Math.floor(seconds / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        return `${m}:${s}`;
    }, [status?.timer_seconds]);

    const foundCount = status?.answers_found?.length ?? 0;
    const totalCount = foundCount + (status?.remaining_answers ?? 0);

    return (
        <div className="ff-overlay">

            {hasBoard ? (
                <>
                    <div className="ff-category">
                        {board.category || ""}
                    </div>

                    <div className="ff-question">
                        {board.survey_question}
                    </div>

                    <div
                        className="ff-answers"
                        aria-label="Friendly Feud answers"
                    >
                        {answers.map((answer) => (
                            <AnswerPlaque
                                key={answer.id}
                                rank={answer.rank}
                                answer={answer.answer}
                                points={answer.points}
                                revealed={answer.revealed}
                            />
                        ))}
                    </div>
                </>
            ) : (
                <div className="ff-empty">
                    Waiting for next board…
                </div>
            )}

            {status?.question_open && (
                <div className="ff-status-bar">
                    <span className="live-indicator">🟢 LIVE</span>
                    <span className="ff-timer">⏱ {timer}</span>
                    <span className="ff-found">✓ {foundCount}/{totalCount}</span>
                </div>
            )}

        </div>
    );
}
