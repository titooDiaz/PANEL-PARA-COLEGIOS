document.addEventListener("DOMContentLoaded", function() {
    var passwordInput = document.getElementById("password");
    var password1Input = document.getElementById("id_password1");
    var password2Input = document.getElementById("id_password2");
    var passwordValue = passwordInput.value;
        password1Input.value = passwordValue;
        password2Input.value = passwordValue;

    passwordInput.addEventListener("input", function() {
        passwordValue = passwordInput.value;
        password1Input.value = passwordValue;
        password2Input.value = passwordValue;
    });
});