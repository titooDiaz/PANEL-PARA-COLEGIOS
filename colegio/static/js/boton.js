const myButtons = document.querySelectorAll('.myButton');   
myButtons.forEach((button) => {
button.addEventListener('click', () => {
    setTimeout(() => {
    button.blur();
    console.log('ok')
    }, 100);
});
});