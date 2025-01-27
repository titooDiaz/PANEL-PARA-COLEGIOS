
document.addEventListener('DOMContentLoaded', function () {
    var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    const locate = document.querySelectorAll('.time_locate');
    const zone_locate = document.getElementById('time_locate');
    const form_zone = document.getElementById('location_time_zone');
    form_zone.value = timezone;

    zone_locate.innerHTML = timezone;

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

            form_zone.value = timezone;
            
        } else {
            zone.forEach(element => {
                element.classList.remove('hidden');
            });
            locate.forEach(element => {
                element.classList.add('hidden');
            });
            form_zone.value = "";
            // Aquí puedes poner el código que deseas ejecutar cuando el checkbox esté desmarcado
        }
    });

});