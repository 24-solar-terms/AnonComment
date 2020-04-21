function listen_delete_comments() {
    /*管理员删除评论监听事件*/
    $(".delete").click(function () {
        if(confirm("确定要删除这条评论吗？")) {
            /*获得评论的c_id*/
            var delete_button = $(this);
            var c_id = delete_button.prev().text();
            $.ajax({
                    url: '/delete',
                    data: {'c_id': c_id},
                    type: 'GET',
                    success: function(data) {
                        if(data === "delete succeed!") {
                            delete_button.closest(".message").css("display", "none");
                            delete_button.closest(".reported_comment").css("display", "none");
                        }
                        else {
                            alert("评论删除失败，去查看一下数据库出现了错误");
                        }
                    }
            });
        }
    });
}

function listen_report_comments() {
    /*监听用户举报事件*/
    $(".report").click(function () {
        var report_button = $(this);
        if(report_button.attr("flag") === "1") {
            alert("您已经举报过该评论了");
        }
        else {
            var c_id = report_button.next().text();
            $.ajax({
                    url: '/report',
                    data: {'c_id': c_id},
                    type: 'GET',
                    success: function(data) {
                        if(data === "report succeed!") {
                            alert("举报成功，感谢您的监督")
                            report_button.attr("flag", "1");
                        }
                        else {
                            alert("举报失败");
                        }
                    }
            });
        }
    });
}

function listen_ignore_comments() {
    /*监听忽略某条举报的评论*/
    $(".ignore").click(function () {
        var ignore_button = $(this);
        var c_id = ignore_button.prev().text();
        $.ajax({
                url: '/ignore',
                data: {'c_id': c_id},
                type: 'GET',
                success: function(data) {
                    if(data === "ignore succeed!") {
                        ignore_button.closest(".reported_comment").css("display", "none");
                    }
                    else {
                        alert("忽略失败，去查看一下数据库出现了错误");
                    }
                }
        });
    });
}

$(function () {
    listen_delete_comments();
    listen_report_comments();
    listen_ignore_comments();
});