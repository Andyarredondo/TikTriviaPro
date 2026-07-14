import React from "react";

import AnswerPlaque from "../AnswerPlaque";
import BroadcastLayout from "../BroadcastLayout";
import QuestionScroll from "../QuestionScroll";

import "../../theme/overlay.css";

export default function FriendlyFeudOverlay({
    board,
    status,
}) {
    const answers = board?.answers ?? [];

    return (
        <BroadcastLayout
            title="Andy the Renaissance Man"
            subtitle="Friendly Feud"
            status={status}
        >
            <div className="overlay-board">

                <div className="overlay-category">
                    {board?.category || "Waiting for category"}
                </div>

                <QuestionScroll
                    category=""
                    question={
                        board?.survey_question ||
                        "Waiting for the next board..."
                    }
                />

                <section
                    aria-label="Friendly Feud answers"
                >
                    {answers.length === 0 ? (
                        <div className="answer-plaque">
                            <div className="answer-rank">
                                —
                            </div>

                            <div className="answer-text">
                                Waiting for answers
                            </div>

                            <div className="answer-score" />
                        </div>
                    ) : (
                        answers.map((answer) => (
                            <AnswerPlaque
                                key={answer.id}
                                rank={answer.rank}
                                answer={answer.answer}
                                points={answer.points}
                                revealed={answer.revealed}
                            />
                        ))
                    )}
                </section>

                <div
                    className="overlay-board-code"
                    aria-label="Board ID"
                >
                    {board?.board_id || "No board loaded"}
                </div>

            </div>
        </BroadcastLayout>
    );
}
