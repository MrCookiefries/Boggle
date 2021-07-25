const $guessForm = $("#guess form");
const $guessInput = $guessForm.find("#word");
const $statusSection = $("#status");
const $resultSpan = $statusSection.find("#result");
const $scoreSpan = $("#score");
const $highScoreSpan = $("#high-score");
const $playedSpan = $("#played");

class Game {
    constructor() {
        this.totalScore = 0;
        this.seconds = 0;
        this.canGuess = true;
        this.timerId = setInterval(this.tick, 1000)
    }

    tick() {
        this.seconds++;
        if (this.seconds >= 60) {
            clearInterval(this.timerId);
            this.canGuess = false;
            this.gameOver();
        }
    }

    async gameOver() {
        let res;
        try {
            res = await axios.post("/update", {score: totalScore});
        } catch (e) {
            console.log(e);
        }
        const {played, score} = res.data;
        $highScoreSpan.text(score);
        $playedSpan.text(played);
    }

    handleGuessForm(e) {
        e.preventDefault();
        if (!this.canGuess) return;
        const word = $guessInput.val();
        $guessInput.val("");
        this.guessWord(word);
    }

    async guessWord(word) {
        let res;
        try {
            res = await axios.get("/guess", {params: {word}});
        } catch (e) {
            console.log(e);
        }
        const result = res.data.result;
        this.showResult(result);
        if (result === "ok") this.updateScore(word);
    }

    showResult(result) {
        if (result === "ok") result = "found";
        else if (result === "not-on-board") result = "not on the board";
        else if (result === "not-word") result = "not a valid word";
        else console.error(result, "does not match any cases in showResults()");
        $resultSpan.text(result);
    }

    updateScore(word) {
        this.totalScore += word.length;
        $scoreSpan.text(this.totalScore);
    }
}

const game = new Game();
$guessForm.on("submit", game.handleGuessForm.bind(game));

