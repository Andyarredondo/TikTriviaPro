import React from "react";

import BroadcastTitle from "./BroadcastTitle";
import DecorativeFrame from "./DecorativeFrame";
import StatusBar from "./StatusBar";

import "../theme/theme.css";
import "../theme/decorative-frame.css";

export default function BroadcastLayout({
    title = "Andy the Renaissance Man",
    subtitle = "",
    status,
    children,
}) {
    return (
        <div className="broadcast-layout">
            <div className="broadcast-frame">

                <DecorativeFrame>

                    <BroadcastTitle
                        show={title}
                        game={subtitle}
                    />

                    <main
                        style={{
                            flex: 1,
                            display: "flex",
                            flexDirection: "column",
                            padding: "24px",
                            gap: "20px",
                            overflow: "hidden",
                        }}
                    >
                        {children}
                    </main>

                    <StatusBar status={status} />

                </DecorativeFrame>
            </div>
        </div>
    );
}
