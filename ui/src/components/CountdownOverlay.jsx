import React from "react";
import "../theme/theme.css";

export default function CountdownOverlay({
    seconds = 3,
    visible = false,
    message = "Get Ready!",
}) {
    if (!visible) return null;

    return (
        <div
            style={{
                position: "absolute",
                inset: 0,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "rgba(0,0,0,0.65)",
                zIndex: 1000,
            }}
        >
            <div
                style={{
                    textAlign: "center",
                    padding: "40px",
                    border: "3px solid var(--rrn-gold)",
                    borderRadius: "20px",
                    background: "rgba(20,20,20,.92)",
                    boxShadow: "0 0 30px rgba(212,175,55,.25)",
                }}
            >
                <div
                    style={{
                        color: "var(--rrn-ivory)",
                        fontSize: "1.4rem",
                        letterSpacing: "2px",
                        marginBottom: "18px",
                    }}
                >
                    {message}
                </div>

                <div
                    style={{
                        color: "var(--rrn-gold)",
                        fontSize: "5rem",
                        fontWeight: "bold",
                        lineHeight: 1,
                    }}
                >
                    {seconds}
                </div>
            </div>
        </div>
    );
}
