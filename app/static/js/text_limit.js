$(function() {
    $("#comment_bar").focus(function() {
        $("#text-count-tip").css("visibility", "visible");
    });
    $("#comment_bar").blur(function() {
        $("#text-count-tip").css("visibility", "hidden");
    });
    $("#comment_bar").on("input propertychange", function() {
        var $this = $(this),
            count = "";
        if($this.val().length > 300) {
            $this.val($this.val().substring(0, 300));
        }
        count = 300 - $this.val().length;
        $("#text-count").text(count);
    });
});