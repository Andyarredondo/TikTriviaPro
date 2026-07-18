/*
==========================================================
TikTrivia Pro
API Service
Version 1.2
==========================================================
*/

async function request(url, options = {}) {
    let response;

    try {
        response = await fetch(url, {
            ...options,
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                ...(options.headers || {}),
            },
        });
    } catch {
        throw new Error(`Network request failed for ${url}.`);
    }

    const responseText = await response.text();
    let payload = null;

    if (responseText.trim()) {
        try {
            payload = JSON.parse(responseText);
        } catch {
            throw new Error(
                `Server returned an invalid response (${response.status}) for ${url}.`
            );
        }
    }

    if (!response.ok || payload?.success === false) {
        throw new Error(
            payload?.detail ||
                payload?.message ||
                `Request failed (${response.status}) for ${url}.`
        );
    }

    if (payload && typeof payload === "object" && "data" in payload) {
        return payload.data;
    }

    return payload;
}

export const api = {
    gameEngines: {
        list() {
            return request("/api/game-engines");
        },
    },

    contestants: {
        list() {
            return request("/api/contestants/");
        },

        create(data) {
            return request("/api/contestants/", {
                method: "POST",
                body: JSON.stringify(data),
            });
        },

        adjustScore(contestantId, amount) {
            return request(`/api/contestants/${contestantId}/adjust-score`, {
                method: "POST",
                body: JSON.stringify({ amount }),
            });
        },

        undoLastScore(contestantId) {
            return request(`/api/contestants/${contestantId}/undo-last-score`, {
                method: "POST",
            });
        },

        setActive(contestantId, active) {
            return request(`/api/contestants/${contestantId}/active?active=${active}`, {
                method: "POST",
            });
        },

        remove(contestantId) {
            return request(`/api/contestants/${contestantId}`, {
                method: "DELETE",
            });
        },
    },

    productions: {
        list() {
            return request("/api/productions");
        },

        get(productionId) {
            return request(`/api/productions/${productionId}`);
        },

        create(data) {
            return request("/api/productions", {
                method: "POST",
                body: JSON.stringify(data),
            });
        },

        update(productionId, data) {
            return request(`/api/productions/${productionId}`, {
                method: "PUT",
                body: JSON.stringify(data),
            });
        },

        remove(productionId) {
            return request(`/api/productions/${productionId}`, {
                method: "DELETE",
            });
        },
    },

    productionPlayback: {
        start(productionId) {
            return request(`/api/production-playback/start/${productionId}`, {
                method: "POST",
            });
        },

        current() {
            return request("/api/production-playback/current");
        },

        next() {
            return request("/api/production-playback/next", {
                method: "POST",
            });
        },

        previous() {
            return request("/api/production-playback/previous", {
                method: "POST",
            });
        },

        end() {
            return request("/api/production-playback/end", {
                method: "POST",
            });
        },
    },

    familyFeud: {
        current() {
            return request("/api/family-feud/current");
        },

        status() {
            return request("/api/family-feud/status");
        },

        firstBoard() {
            return request("/api/family-feud/first", {
                method: "POST",
            });
        },

        previousBoard() {
            return request("/api/family-feud/previous", {
                method: "POST",
            });
        },

        nextBoard() {
            return request("/api/family-feud/next", {
                method: "POST",
            });
        },

        randomDeckNew() {
            return request("/api/family-feud/random-deck/new", {
                method: "POST",
            });
        },

        randomDeckNext() {
            return request("/api/family-feud/random-deck/next", {
                method: "POST",
            });
        },

        randomDeckStatus() {
            return request("/api/family-feud/random-deck/status");
        },

        openRound() {
            return request("/api/family-feud/open", {
                method: "POST",
            });
        },

        closeRound() {
            return request("/api/family-feud/close", {
                method: "POST",
            });
        },

        resetRound() {
            return request("/api/family-feud/reset", {
                method: "POST",
            });
        },

        revealRemaining() {
            return request("/api/family-feud/reveal_remaining", {
                method: "POST",
            });
        },

        revealAnswer(rank) {
            return request(`/api/family-feud/reveal/${rank}`, {
                method: "POST",
            });
        },

        setRegistrationMode(mode) {
            return request(`/api/family-feud/registration_mode/${mode}`, {
                method: "POST",
            });
        },

        getBoardSource() {
            return request("/api/family-feud/board-source");
        },

        getCategories() {
            return request("/api/family-feud/categories");
        },

        setBoardSource(source) {
            return request(`/api/family-feud/board-source/${source}`, {
                method: "POST",
            });
        },

        setCategorySource(category) {
            return request(
                `/api/family-feud/board-source/category/${encodeURIComponent(category)}`,
                {
                    method: "POST",
                }
            );
        },
    },
};