async function nextBoard(){

    const response = await fetch(
        "/api/family-feud/next",
        {
            method:"POST"
        }
    );

    const board = await response.json();

    document.getElementById("board-id").innerText =
        board.board_id;

    document.getElementById("category").innerText =
        board.category;

    document.getElementById("survey-question").innerText =
        board.survey_question;

    for(let i=1;i<=5;i++){

        document.getElementById(
            "answer"+i
        ).innerText="██████████████████";

    }

    document.getElementById(
        "status"
    ).innerText="Board Loaded";
}

document
.getElementById("next-board")
.onclick=nextBoard;