$(function() {
    /*js前端检查表单是否满足提交条件*/
    var check = function() {
        var score = $("#score").val();
        var whether_call_roll = $("input[name='whether_call_roll']:checked").val();
        if(score === "-1" && whether_call_roll === undefined) {
            $("#error").text(" * 请给老师一个评分并选择该老师是否会点名");
            return false;
        }
        else if(score === "-1") {
            $("#error").text(" * 请给老师一个评分");
            return false;
        }
        else if(whether_call_roll === undefined) {
            $("#error").text(" * 请选择老师是否点名");
            return false;
        }
        /*获取提交时间*/
        var now = new Date();
        var y = now.getFullYear(),
            m = now.getMonth() + 1,
            d = now.getDate();
        var date = y + "-" + m + "-" + d;
        $("#submit_date").val(date);
        alert("评论成功！");
        return true;
    }
    $("#submit").click(check);
    /*用户修改对老师的评价时，点击修改按钮，发送ajax*/
    $("#edit_button").click(function () {
        /*保存原值*/
        var score = $("#user_score").text();
        var call_roll = $("#user_call_roll").text();
        var comment = $("#comment_bar").val();
        $.ajax({
                url: '/update_user_comment',
                type: 'GET',
                success: function(data) {
                    /*获取提交表单后，各项初始化为原值*/
                    $(".comment_form").html(data);
                    $("#comment_form").attr("action", "/update_user_comment");
                    $("#score").val(parseInt(score));
                    if(call_roll === "会") {
                        $('input:radio').eq(0).attr('checked', 'true');
                    }
                    else {
                        $('input:radio').eq(1).attr('checked', 'true');
                    }
                    $("#comment_bar").val(comment);
                    /*设置点击事件*/
                    $("#submit").click(check);
                }
        });
    });
});