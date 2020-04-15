$(function() {
    /*点击发送ajax请求，获取不同的Jinja模板片段*/
    $("#hot_comments").click(function() {
        if($(this).attr("flag") === "0"){
            /*设置两按钮互斥*/
            $(this).attr("flag", "1");
            $(this).css("color", "black");
            var newest_comments = $(this).next();
            newest_comments.attr("flag", "0");
            newest_comments.css("color", "gray");
            $.ajax({
                url: '/rank',
                data: {'way': '0'},
                type: 'GET',
                success: function(data) {
                    $("#messages").html(data);
                },
                complete: function() {
                    /*重新设置点赞的监听事件*/
                    like_func();
                }
            });
        }
    });
    $("#newest_comments").click(function() {
        if($(this).attr("flag") === "0"){
            /*设置两按钮互斥*/
            $(this).attr("flag", "1");
            $(this).css("color", "black");
            var hot_comments = $(this).prev();
            hot_comments.attr("flag", "0");
            hot_comments.css("color", "gray");
            $.ajax({
                url: '/rank',
                data: {'way': '1'},
                type: 'GET',
                success: function(data) {
                    $("#messages").html(data);
                },
                complete: function() {
                    /*重新设置点赞的监听事件*/
                    like_func();
                }
            });
        }
    });
});