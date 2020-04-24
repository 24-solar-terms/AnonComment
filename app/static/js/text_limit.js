function listen_text_num() {
    /*文本框获取焦点显示剩余和输入字数，失去焦点不显示*/
    $("#comment_bar").focus(function() {
        $("#text-count-tip").css("visibility", "visible");
    });
    $("#comment_bar").blur(function() {
        $("#text-count-tip").css("visibility", "hidden");
    });
    /*监听文本框的内容改变，并显示剩余字数，超过规定字数则截断*/
    $("#comment_bar").on("input propertychange", function() {
        var $this = $(this),
            count = "";
        if($this.val().length > 300) {
            $this.val($this.val().substring(0, 300));
        }
        count = 300 - $this.val().length;
        $("#text-count").text(count);
    });
}

$(function() {
    listen_text_num();
});