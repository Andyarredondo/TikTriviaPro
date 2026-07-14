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
                            padding: "3% 3% 2%",
                            gap: "2%",
                            overflow: "hidden",
                            minHeight: 0,
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
