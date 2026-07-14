import React from "react";
import "../theme/theme.css";

export default function BroadcastHeader({
    title="Andy the Renaissance Man",
    subtitle="Friendly Feud",
    status
}) {

    const seconds = status?.timer_seconds ?? 0;
    const mm = String(Math.floor(seconds/60)).padStart(2,"0");
    const ss = String(seconds%60).padStart(2,"0");

    return (
        <header className="broadcast-header">

            <div className="broadcast-left">
                <div className="live-indicator">
                    {status?.question_open ? "● LIVE" : "● CLOSED"}
                </div>
            </div>

            <div className="broadcast-center">
                <h1 className="broadcast-title">{title}</h1>
                <div className="broadcast-subtitle">{subtitle}</div>
            </div>

            <div className="broadcast-right">
                <div className="timer">
                    ⏱ {mm}:{ss}
                </div>
            </div>

        </header>
    );
}
