const endDate = document.getElementById('end-time');

let countDownDate = new Date(endDate.value).getTime()

// ADDING 30 DAYS FROM NOW
// var now = new Date();
// var THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;
// var thirtyDaysFromNow = now + THIRTY_DAYS;

const countDown = setInterval(() => {
    let now = new Date().getTime();
    let timeLeft = countDownDate - now;
    
    let days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    let hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        
    document.getElementById("days").innerHTML = days + " :"
    document.getElementById("hours").innerHTML = hours + " :" 
    document.getElementById("mins").innerHTML = minutes + " :" 
    document.getElementById("secs").innerHTML = seconds + ""
    
    if(timeLeft < 0){
        clearInterval(countDown)
        document.getElementById("days").innerHTML = ""
        document.getElementById("hours").innerHTML = "" 
        document.getElementById("mins").innerHTML = ""
        document.getElementById("secs").innerHTML = ""
        console.log('here')
        window.location.reload();
    }

}, 1000)