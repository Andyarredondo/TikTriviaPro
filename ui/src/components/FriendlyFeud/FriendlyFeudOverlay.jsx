import React from "react";

import AnswerPlaque from "../AnswerPlaque";
import BroadcastLayout from "../BroadcastLayout";
import CategoryRibbon from "../CategoryRibbon";
import EmptyBoard from "../EmptyBoard";
import QuestionScroll from "../QuestionScroll";

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

    return (
        <BroadcastLayout
            title="Andy the Renaissance Man"
            subtitle=""
            status={status}
        >
            <div className="overlay-board">
                {!hasBoard ? (
                    <EmptyBoard />
                ) : (
                    <>
                        <CategoryRibbon
                            category={board.category}
                        />

                        <QuestionScroll
                            category=""
                            question={board.survey_question}
                        />

                        <section
                            className="overlay-answer-list"
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
                        </section>

                        <div
                            className="overlay-board-code"
                            aria-label="Board ID"
                        >
                            Board {board.board_id}
                        </div>
                    </>
                )}
            </div>
        </BroadcastLayout>
    );
}
