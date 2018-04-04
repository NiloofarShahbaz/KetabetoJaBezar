/**
 * Created by sunset on 30/03/2018.
 */
$(document).ready(function(){
    $(window).bind('scroll', function() {
        var navHeight = $( window ).height() - 70;
        if ($(window).scrollTop() > navHeight) {
            $('nav').addClass('fixed');
        }
        else {
            $('nav').removeClass('fixed');
        }
    });
});

/*------------------------botton-------------------------------------*/
/* Best with Chrome :/ */


$('.button-sivir').on('click', function(e) {
    $("#loader").attr("class", "loading");
    $("#loader-g").attr("class", "zindex");
    e.stopPropagation();
});

$(document).click(function() {
    $("#loader").attr("class", "");
    $("#loader-g").attr("class", "");
});

$('.button-singed').on('click', function(e) {
    $("#tick").attr("class", "stroke-tick");
    e.stopPropagation();
});

$(document).click(function() {
    $("#tick").attr("class", "");
});