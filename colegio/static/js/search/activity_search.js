// past tasks

var searchPastInput = document.getElementById("search_past_activities");
var PastTasks = document.querySelectorAll('#PastTask');

searchPastInput.addEventListener("input", function () {
    var searchPastTerm = searchPastInput.value.toLowerCase();

    PastTasks.forEach(function (task) {
        var namePastElement = task.querySelector('#PastName');
        var divPastContenedor = task;

        var labelPastText = namePastElement?.innerText.toLowerCase();

        if (labelPastText && labelPastText.includes(searchPastTerm)) {
            divPastContenedor.classList.remove('hidden');
        } else {
            divPastContenedor.classList.add('hidden');
        }
    });
});

// recent tasks

var searchRecentInput = document.getElementById("search_recent_activities");
var RecentTasks = document.querySelectorAll('#RecentTask');

searchRecentInput.addEventListener("input", function () {
    var searchRecentTerm = searchRecentInput.value.toLowerCase();

    RecentTasks.forEach(function (task) {
        var nameElement = task.querySelector('#RecentName');
        var divRecentContenedor = task;

        var labelRecentText = nameElement?.innerText.toLowerCase();

        if (labelRecentText && labelRecentText.includes(searchRecentTerm)) {
            divRecentContenedor.classList.remove('hidden');
        } else {
            divRecentContenedor.classList.add('hidden');
        }
    });
});
