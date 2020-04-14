$(function () {
    var timeout;
    /*发送ajax请求，传入查找的关键词*/
    function get_matched_data() {
        var val = $("#search_bar").val();
        if(val !== "") {
            $.ajax({
                url: '/search',
                data: {
                        'tip': '1',
                        'keyword': val
                      },
                type: 'GET',
                success: function(data) {
                    /*成功获得数据后显示提示框*/
                    $(".search_tip_box").css("display", "block");
                    $(".search_tip_box").html(data);
                }
            });
        }
    }
    /*监听搜索框值的变化并且延迟半秒发送请求，小于半秒的值改变将作废不会发送请求*/
	$("#search_bar").on("input propertychange", function() {
	    clearTimeout(timeout);
        timeout = setTimeout(function () {
            get_matched_data();
        }, 500);
    });
    /*搜索框获取焦点，发送请求*/
    $("#search_bar").focus(function () {
        get_matched_data();
    });
    /*点击搜索框和提示框以外的元素，提示框消失*/
    $(document).bind("click", function (e) {
        if($(e.target).closest("#search_bar").length === 0 && $(e.target).closest(".search_tip_box").length === 0) {
            $(".search_tip_box").css("display", "none");
        }
    });
});