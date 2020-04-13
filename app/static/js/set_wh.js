$(function(){
    /*设定body的固定宽高，禁止缩放*/
    var body = $('body');
    var screen_height = window.innerHeight;
    var screen_width = window.screen.availWidth;
    body.css('height', screen_height);
    /*窗口出现滚动条时对body宽度进行调整，即原宽度减去滚动条宽度*/
    if(document.body.scrollHeight > (window.innerHeight || document.documentElement.clientHeight)) {
        body.css('width', screen_width - (window.innerWidth - document.body.clientWidth));
    }
    else {
        body.css('width', screen_width);
    }
    
});