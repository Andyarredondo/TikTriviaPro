import React, { useCallback, useEffect, useState } from "react";

import { api } from "../../services/api";
import FriendlyFeudOverlay from "../../components/FriendlyFeud/FriendlyFeudOverlay";
import StandbyOverlay from "../../components/FriendlyFeud/StandbyOverlay";

import "../../theme/theme.css";
import "../../theme/overlay.css";

export default function ViewerOverlay() {

    const [board, setBoard] = useState(null);
    const [status, setStatus] = useState(null);

    // theme.css sets html,body,#root { height:100% } and body { overflow:hidden }
    // and a dark body background — all designed for the host dashboard.
    // Override those here so the overlay page sizes to its content and the body
    // is transparent so the stream shows through.
    
    const refresh = useCallback(async () => {
        try {
            const s = await api.familyFeud.status();
            setStatus(s);

            if (s.board_loaded) {
                const b = await api.familyFeud.current();
                setBoard(b);
            } else {
                setBoard(null);
            }
        } catch (err) {
            console.error(err);
        }
    }, []);

    useEffect(() => {
        refresh();
        const id = window.setInterval(refresh, 500);
        return () => window.clearInterval(id);
    }, [refresh]);

    return (
    <div
        style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "flex-start",
            padding: "18px",
            boxSizing: "border-box",
            background: "transparent",
        }}
    >
        <div
            style={{
                width: "min(900px, calc(100vw - 36px))",
                flexShrink: 0,
            }}
        >
                {status?.viewer_overlay_state === "STANDBY" ? (
                    <StandbyOverlay />
                ) : (
                    <FriendlyFeudOverlay
                        board={board}
                        status={status}
                    />
                )}
            </div>
        </div>
    );
}
