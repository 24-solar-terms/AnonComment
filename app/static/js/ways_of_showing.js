$(function() {
    $("#hot_comments").click(function() {
        if($(this).attr("flag") === "0"){
            $(this).attr("flag", "1");
            $(this).css("color", "black");
            var newest_comments = $(this).next();
            newest_comments.attr("flag", "0");
            newest_comments.css("color", "gray");
            $.ajax({
                url: '/rank',
                data: {'way': '0'},
                type: 'POST',
                success: function(data) {
                    $("#messages").html(data);
                },
                complete: function() {
                    like_func();
                }
            });
        }
    });
    $("#newest_comments").click(function() {
        if($(this).attr("flag") === "0"){
            $(this).attr("flag", "1");
            $(this).css("color", "black");
            var hot_comments = $(this).prev();
            hot_comments.attr("flag", "0");
            hot_comments.css("color", "gray");
            $.ajax({
                url: '/rank',
                data: {'way': '1'},
                type: 'POST',
                success: function(data) {
                    $("#messages").html(data);
                },
                complete: function() {
                    like_func();
                }
            });
        }
    });
});