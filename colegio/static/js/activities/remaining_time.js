const COUNTDOWN_FROM = document.getElementById('date').textContent;
console.log(COUNTDOWN_FROM);
const SECOND = 1000;
const MINUTE = SECOND * 60;
const HOUR = MINUTE * 60;
const DAY = HOUR * 24;

const updateCountdown = () => {
const end = new Date(COUNTDOWN_FROM);
const now = new Date();
const distance = end - now;

const days = Math.floor(distance / DAY);
const hours = Math.floor((distance % DAY) / HOUR);
const minutes = Math.floor((distance % HOUR) / MINUTE);
const seconds = Math.floor((distance % MINUTE) / SECOND);

document.getElementById("days").textContent = days;
document.getElementById("hours").textContent = hours;
document.getElementById("minutes").textContent = minutes;
document.getElementById("seconds").textContent = seconds;
};

setInterval(updateCountdown, 1000);
updateCountdown(); 