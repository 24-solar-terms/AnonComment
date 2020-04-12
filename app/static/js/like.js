$(function() {
    var like_dict = {};
    var old_like = {}
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
    /*点击点赞按钮的事件*/
    $(".good").click(function() {
        if($(this).attr("flag") === "0"){
            $(this).attr("flag", "1");
            $(this).css({"margin-top": "-10px", "margin-bottom": "15px"});
            var p = $(this).next();
            var new_num = parseInt(p.text()) + 1;
            p.text(new_num);
            p.css("color", "rgb(253, 54, 104)");
            if($(this).attr("id") in like_dict) {
                like_dict[$(this).attr("id")] += 1;
            }
            else {
                like_dict[$(this).attr("id")] = 1;
                old_like[$(this).attr("id")] = 0;
            }
        }
        else {
            $(this).attr("flag", "0");
            $(this).css("margin", "0 auto");
            var p = $(this).next();
            var new_num = parseInt(p.text()) - 1;
            p.text(new_num);
            p.css("color", "black");
            if($(this).attr("id") in like_dict) {
                like_dict[$(this).attr("id")] += 1;
            }
            else {
                like_dict[$(this).attr("id")] = 1;
                old_like[$(this).attr("id")] = 1;
            }
        }
    });
    /*窗口销毁后发起ajax请求，提交数据库*/
    window.onunload = function () {
        for(var key in like_dict) {
            if(like_dict[key] % 2 === 0) {
                delete like_dict[key];
            }
            else {
                if(old_like[key] === 0) {
                    like_dict[key] = 1;
                }
                else {
                    like_dict[key] = 0;
                }
            }
        }
        $.ajax({
            url: '/save_user_support',
            data: like_dict,
            type: 'GET'
        });
    }
});