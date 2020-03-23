$(function(){
    var body = $('body');
    var screen_height = window.innerHeight;
    var screen_width = window.screen.width;
    body.css('height', screen_height);
    if(document.body.scrollHeight > (window.innerHeight || document.documentElement.clientHeight)) {
        body.css('width', screen_width-17);
    }
    else {
        body.css('width', screen_width);
    }
    
});