
    document.addEventListener('DOMContentLoaded', function () {
        // Obtener la zona horaria del navegador
        var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        // Establecer el valor del campo oculto de zona horaria
        document.getElementById("time_locate").innerHTML=timezone;
        //document.getElementById('id_timezone').value = timezone;
        console.log(timezone)
    });