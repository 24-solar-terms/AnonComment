$(function() {
    $("#by_depart").click(function() {
        if($(this).attr("flag") === "0") {
            $(this).attr("flag", "1");
            $("#by_rank").attr("flag", "0");
            $.ajax({
                url: '/ways',
                type: 'POST',
                data: {'ways': '0'},
                success: function(data) {
                    $("#show_teachers").html(data);
                }
            });
        }
    });
    $("#by_rank").click(function() {
        if($(this).attr("flag") === "0") {
            $(this).attr("flag", "1");
            $("#by_depart").attr("flag", "0");
            $.ajax({
                url: '/ways',
                type: 'POST',
                data: {'ways': '1'},
                success: function(data) {
                    $("#show_teachers").html(data);
                }
            });
        }
    });
});