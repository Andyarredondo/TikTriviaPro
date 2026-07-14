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

    },

};