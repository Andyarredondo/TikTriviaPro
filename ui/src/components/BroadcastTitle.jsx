import React from "react";
import logo from "../assets/logos/tiktriviapro-logo.svg";
import "../theme/theme.css";

export default function BroadcastTitle({
    show = "Andy the Renaissance Man",
    game = "",
}) {
    return (
        <section
            style={{
                textAlign: "center",
                padding: "2.5% 4% 1.5%",
                borderBottom: "2px solid var(--rrn-gold-dark)",
                flexShrink: 0,
            }}
        >
            <img
                src={logo}
                alt={show}
                style={{
                    height: "clamp(36px, 8cqw, 64px)",
                    width: "auto",
                    display: "block",
                    margin: "0 auto",
                    objectFit: "contain",
                    filter: "drop-shadow(0 0 8px rgba(212,175,55,.4))",
                }}
            />

            {game && (
                <div
                    style={{
                        marginTop: "6px",
                        color: "var(--rrn-ivory)",
                        fontSize: "clamp(0.75rem, 2.5cqw, 1.25rem)",
                        letterSpacing: "2px",
                    }}
                >
                    {game}
                </div>
            )}
        </section>
    );
}
