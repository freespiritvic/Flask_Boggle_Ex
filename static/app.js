"use strict";

let score = 0
let words = new Set()

let time = 60
$('#timer').html(time);

$('form').on('submit', handleSubmit);

async function handleSubmit(e) {
    e.preventDefault();
    let word = $('input').val();
    if(!word) return;
    const res = await axios.get('/word_check', {params: {word: word}});
    let response = res.data.result;
    $('#response').text(response)
    $('form').trigger('reset')
    if (response === 'ok') {
        if (words.has(word)) {
            return;
        }
        words.add(word)
        score += word.length;
        $('#score').html(`Score: ${score}`);
    }
}


let countDown = setInterval(function () {
    time--;
    $('#timer').html(time);
    stopTimer();
}, 1000);

function stopTimer() {
    if (time < 1) {
        clearInterval(countDown);
        $('form').hide();
        $('.container').append($('<span>').html('Game Over!!!'));
        gameOver()
    }
}

async function gameOver() {
    await axios.post('/game_over', {score: score})
}












