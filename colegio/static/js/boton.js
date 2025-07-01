// Global click handler for all <a> and <button> elements
document.addEventListener('click', (e) => {
    const el = e.target.closest('a, button');
    if (el) {
        console.log("Clicked element:", el);

        // Trigger vibration (if supported and on mobile)
        navigator.vibrate?.([40]);

        // Remove focus after a short delay
        setTimeout(() => el.blur(), 100);
    }
});
