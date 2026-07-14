/*
==========================================================
TikTrivia Pro
API Service
Version 1.1
==========================================================
*/

async function request(url, options = {}) {

    const response = await fetch(url, {

        headers: {
            "Content-Type": "application/json",
        },

        ...options,

    });

    const payload = await response.json();

    if (!response.ok || payload.success === false) {

        throw new Error(

            payload.message ||

            `Request failed (${response.status})`

        );

    }

    return payload.data;

}

export const api = {

    contestants: {

        async list() {

            const response = await fetch("/api/contestants/");

            if (!response.ok) {

                throw new Error("Unable to load contestants.");

            }

            return await response.json();

        },

        async resetScore(contestantId) {
            return request(`/api/contestants/${contestantId}/reset_score`, {
                method: "POST",
            });
        },

        async setActive(contestantId, active) {
            return request(`/api/contestants/${contestantId}/active?active=${active}`, {
                method: "POST",
            });
        },

        async remove(contestantId) {
            return request(`/api/contestants/${contestantId}`, {
                method: "DELETE",
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

            return request(`/api/family-feud/board-source/category/${encodeURIComponent(category)}`, {

                method: "POST",

            });

        },

    },

};