
document.addEventListener('DOMContentLoaded', function () {
    var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    const locate = document.querySelectorAll('.time_locate');
    console.log(locate)

    locate.forEach(element => {
        element.innerHTML = timezone;
        console.log()
    });

    const zone = document.querySelectorAll('.time_zone');
    console.log(zone)


    const checkbox = document.getElementById('zona_horaria');

    checkbox.addEventListener('change', (event) => {
        if (event.target.checked) {
            zone.forEach(element => {
                element.classList.add('hidden');
            });
            locate.forEach(element => {
                element.classList.remove('hidden');
            });
            
        } else {
            zone.forEach(element => {
                element.classList.remove('hidden');
            });
            locate.forEach(element => {
                element.classList.add('hidden');
            });
            // Aquí puedes poner el código que deseas ejecutar cuando el checkbox esté desmarcado
        }
    });

});