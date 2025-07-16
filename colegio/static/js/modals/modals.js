document.getElementById('active_information').addEventListener('click', function() {
    var infoDiv = document.getElementById('information');
    
    if (infoDiv.classList.contains('hidden')) {
        infoDiv.classList.remove('hidden');
    } else {
        infoDiv.classList.add('hidden');
    }
});

document.getElementById('close_information').addEventListener('click', function() {
    var close_div = document.getElementById('information');
    close_div.classList.add('hidden');
});