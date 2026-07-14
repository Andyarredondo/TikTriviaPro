import React from "react";
import "../theme/theme.css";

export default function BroadcastTitle({
    show = "Andy the Renaissance Man",
    game = "",
}) {
    return (
        <section
            style={{
                textAlign: "center",
                padding: "14px 24px 22px",
                borderBottom: "2px solid var(--rrn-gold-dark)",
                marginBottom: "18px",
            }}
        >
            <div
                style={{
                    color: "var(--rrn-gold)",
                    fontFamily: 'Georgia,"Times New Roman",serif',
                    fontSize: "2.2rem",
                    fontWeight: 700,
                    letterSpacing: "4px",
                    textTransform: "uppercase",
                    textShadow: "0 0 10px rgba(212,175,55,.35)"
                }}
            >
                {show}
            </div>

            {game && (
                <div
                    style={{
                        marginTop: "8px",
                        color: "var(--rrn-ivory)",
                        fontSize: "1.25rem",
                        letterSpacing: "2px",
                    }}
                >
                    {game}
                </div>
            )}
        </section>
    );
}
