import React from "react";
import "../theme/theme.css";

export default function GoldDivider({
    label = "",
}) {
    return (
        <div
            style={{
                display: "flex",
                alignItems: "center",
                gap: "16px",
                margin: "18px 0",
            }}
        >
            <div
                style={{
                    flex: 1,
                    height: "2px",
                    background:
                        "linear-gradient(to right, transparent, var(--rrn-gold), transparent)",
                }}
            />

            {label ? (
                <div
                    style={{
                        color: "var(--rrn-gold)",
                        letterSpacing: "3px",
                        textTransform: "uppercase",
                        fontWeight: 700,
                        whiteSpace: "nowrap",
                    }}
                >
                    {label}
                </div>
            ) : null}

            <div
                style={{
                    flex: 1,
                    height: "2px",
                    background:
                        "linear-gradient(to right, transparent, var(--rrn-gold), transparent)",
                }}
            />
        </div>
    );
}
