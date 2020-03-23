var is_loaded = false;
function req() {
    $.ajax({
        url: '/total',
        type: 'GET',
        beforeSend: function() {
            is_loaded = false;
        },
        success: function(data) {
            $("#tot_num").text(data);
        },
        complete: function() {
            is_loaded = true;
        }
    });
}
$(function() {
    req();
    setInterval(function() {
        is_loaded && req();
    }, 3000);
});