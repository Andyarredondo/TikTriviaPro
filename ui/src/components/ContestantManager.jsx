import { useState } from "react";
import { api } from "../services/api";

export default function ContestantManager({
    refreshContestants,
}) {
    const [displayName, setDisplayName] = useState("");
    const [username, setUsername] = useState("");
    const [isWorking, setIsWorking] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    async function addContestant() {
        const cleanedDisplayName = displayName.trim();
        const cleanedUsername =
            username.trim() ||
            cleanedDisplayName
                .toLowerCase()
                .replace(/[^a-z0-9_]+/g, "_")
                .replace(/^_+|_+$/g, "");

        if (!cleanedDisplayName) {
            setErrorMessage("Display name is required.");
            return;
        }

        if (!cleanedUsername) {
            setErrorMessage("Enter a valid TikTok username.");
            return;
        }

        setIsWorking(true);

        try {
            await api.contestants.create({
                username: cleanedUsername,
                display_name: cleanedDisplayName,
            });

            setDisplayName("");
            setUsername("");
            setErrorMessage("");

            await refreshContestants();
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error.message || "Unable to add contestant."
            );
        } finally {
            setIsWorking(false);
        }
    }

    return (
        <div className="contestant-mode">
            <div className="board-control-label">
                Add Contestant
            </div>

            {errorMessage && (
                <div className="placeholder">
                    {errorMessage}
                </div>
            )}

            <div className="board-control-group">
                <input
                    type="text"
                    value={displayName}
                    onChange={(event) =>
                        setDisplayName(event.target.value)
                    }
                    placeholder="Display name"
                    disabled={isWorking}
                />
            </div>

            <div className="board-control-group">
                <input
                    type="text"
                    value={username}
                    onChange={(event) =>
                        setUsername(event.target.value)
                    }
                    placeholder="TikTok username (optional)"
                    disabled={isWorking}
                />
            </div>

            <div className="board-control-row">
                <button
                    type="button"
                    onClick={addContestant}
                    disabled={isWorking}
                >
                    {isWorking
                        ? "Adding..."
                        : "Add Contestant"}
                </button>
            </div>
        </div>
    );
}