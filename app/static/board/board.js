function generateSudoku() {
    const gameboard = document.querySelector("#gameboard");
    const blockTemplate = document.querySelector("#blockTemplate");
    const cellTemplate = document.querySelector("#cellTemplate");

    for (let i = 0; i < 9; i++) {
        let newBlock = blockTemplate.cloneNode(true);
        newBlock.removeAttribute("id")
        gameboard.appendChild(newBlock);
        for (let j = 0; j < 9; j++) {
            let newCell = cellTemplate.cloneNode(true);
            newCell.id = `cell${i}${j}`;
            newBlock.appendChild(newCell);
        }
    }

    blockTemplate.style.display = 'none';
    cellTemplate.style.display = 'none';
}