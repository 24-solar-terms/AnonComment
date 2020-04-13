function like_func() {
    /*显示用户是否已经点赞*/
    var good_button = $(".good");
    for(var i = 0; i < good_button.length; i++) {
        var tmp = $(good_button[i]);
        if(tmp.attr("flag") === "1") {
            tmp.css({"margin-top": "-10px", "margin-bottom": "15px"});
            var p = tmp.next();
            p.css("color", "rgb(253, 54, 104)");
        }
    }
    /*点击点赞按钮的事件，发送ajax请求，保存到数据库*/
    $(".good").click(function() {
        if($(this).attr("flag") === "0"){
            $(this).attr("flag", "1");
            $(this).css({"margin-top": "-10px", "margin-bottom": "15px"});
            var p = $(this).next();
            var new_num = parseInt(p.text()) + 1;
            p.text(new_num);
            p.css("color", "rgb(253, 54, 104)");
            $.ajax({
                url: '/save_user_support',
                type: 'GET',
                data: {
                       'c_id': $(this).attr("id"),
                       'click': 1
                      }
            });
        }
        else {
            $(this).attr("flag", "0");
            $(this).css("margin", "0 auto");
            var p = $(this).next();
            var new_num = parseInt(p.text()) - 1;
            p.text(new_num);
            p.css("color", "black");
            $.ajax({
                url: '/save_user_support',
                type: 'GET',
                data: {
                       'c_id': $(this).attr("id"),
                       'click': 0
                      }
            });
        }
    });
}

$(function() {
    like_func();
});