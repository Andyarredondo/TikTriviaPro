import React from "react";
import "../theme/theme.css";

const HIDDEN = "████████████████████";

export default function AnswerPlaque({
    rank,
    answer,
    points,
    revealed = false,
}) {
    return (
        <div
            className={
                revealed
                    ? "answer-plaque revealed"
                    : "answer-plaque"
            }
        >
            <div className="answer-rank">
                {rank}
            </div>

            <div className="answer-text">
                {revealed
                    ? answer
                    : HIDDEN}
            </div>

            <div className="answer-score">
                {revealed
                    ? points
                    : ""}
            </div>
        </div>
    );
}
