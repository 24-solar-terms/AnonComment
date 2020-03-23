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
});