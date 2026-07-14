import React, { useCallback, useEffect, useLayoutEffect, useState } from "react";

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
    useLayoutEffect(() => {
        const html = document.documentElement;
        const body = document.body;
        const root = document.getElementById("root");

        html.style.height = "auto";
        body.style.height = "auto";
        body.style.overflow = "visible";
        body.style.background = "transparent";
        if (root) root.style.height = "auto";
    }, []);

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
        <div style={{ display: "flex", justifyContent: "center", background: "transparent" }}>
            {/* width-constrained canvas — height follows content naturally */}
            <div style={{ width: "min(100vw, 100vh)", flexShrink: 0 }}>
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
