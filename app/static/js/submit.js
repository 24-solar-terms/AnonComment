$(function() {
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

    $("#edit_button").click(function () {
        var score = $("#user_score").text();
        var call_roll = $("#user_call_roll").text();
        var comment = $("#comment_bar").val();
        $.ajax({
                url: '/update_user_comment',
                type: 'GET',
                success: function(data) {
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
                    $("#submit").click(check);
                }
        });
    });
});