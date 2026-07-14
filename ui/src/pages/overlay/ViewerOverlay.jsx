import React, { useCallback, useEffect, useState } from "react";

import { api } from "../../services/api";
import FriendlyFeudOverlay from "../../components/FriendlyFeud/FriendlyFeudOverlay";

import "../../theme/theme.css";
import "../../theme/overlay.css";

export default function ViewerOverlay() {

    const [board, setBoard] = useState(null);
    const [status, setStatus] = useState(null);

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
                width: "100vw",
                height: "100vh",
                overflow: "hidden",
                background: "#111"
            }}
        >
            <FriendlyFeudOverlay
                board={board}
                status={status}
            />
        </div>
    );
}
