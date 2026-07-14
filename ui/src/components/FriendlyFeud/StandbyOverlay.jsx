import React from "react";

export default function StandbyOverlay() {
    return (
        <div className="standby-overlay">
            <div className="standby-panel">
                <h1 className="standby-title">Next Question</h1>
                <p className="standby-subtitle">Coming Up!</p>
            </div>
        </div>
    );
}
