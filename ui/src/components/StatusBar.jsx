import React, { useMemo } from "react";
import "../theme/theme.css";

export default function StatusBar({
    status,
}) {
    const totalAnswers = useMemo(() => {
        if (!status) return 0;
        return (status.answers_found?.length ?? 0) + (status.remaining_answers ?? 0);
    }, [status]);

    const timer = useMemo(() => {
        const seconds = status?.timer_seconds ?? 0;
        const m = String(Math.floor(seconds / 60)).padStart(2,"0");
        const s = String(seconds % 60).padStart(2,"0");
        return `${m}:${s}`;
    }, [status]);

    return (
        <div className="broadcast-status">
            <div className="live-indicator">
                {status?.question_open ? "● LIVE" : "● CLOSED"}
            </div>

            <div className="timer">
                ⏱ {timer}
            </div>

            <div className="found-counter">
                {status?.answers_found?.length ?? 0}
                {" / "}
                {totalAnswers}
                {" FOUND"}
            </div>
        </div>
    );
}
