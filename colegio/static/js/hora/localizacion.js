
    document.addEventListener('DOMContentLoaded', function () {
        // Obtener la zona horaria del navegador
        var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        // Establecer el valor del campo oculto de zona horaria
        document.getElementById("time_locate").innerHTML=timezone;
        //document.getElementById('id_timezone').value = timezone;

        const date = new Date();
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        console.log(year, month, day)
    });