function like_func() {
    $(".good").click(function() {
        if($(this).attr("flag") === "0"){
            $(this).attr("flag", "1");
            $(this).css({"margin-top": "-10px", "margin-bottom": "15px"});
            var p = $(this).next();
            var new_num = parseInt(p.text()) + 1;
            p.text(new_num);
            p.css("color", "rgb(253, 54, 104)");
        }
        else {
            $(this).attr("flag", "0");
            $(this).css("margin", "0 auto");
            var p = $(this).next();
            var new_num = parseInt(p.text()) - 1;
            p.text(new_num);
            p.css("color", "black");
        }
    });
}
$(function() {
    like_func();
});