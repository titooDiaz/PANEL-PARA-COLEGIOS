// Global click handler that works for any .myButton on the page
document.addEventListener('click', (e) => {
    const button = e.target.closest('.myButton');
    if (button) {
        console.log("Button clicked!");

        // Trigger device vibration
        navigator.vibrate?.([40,20,50]);

        // Optionally remove focus if it's a submit button
        setTimeout(() => button.blur(), 100);
    }
});
