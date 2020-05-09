$(document).ready(function() {

	"use strict"

    $(".owl-carousel").owlCarousel({
      autoPlay: 3000, //Set AutoPlay to 3 seconds
      items: 2,
      navigation: true,
      pagination: false,
      navigationText: ["",""],
      itemsDesktop : [1000,2], //5 items between 1000px and 901px
      itemsDesktopSmall : [900,2], // betweem 900px and 601px
      itemsTablet: [600,1], //2 items between 600 and 0
  })

    $('.toggle-menu').click(function(){
        $('.main-navigation ul').stop(true,true).slideToggle()
    })

    $(window).on('resize', function(){
        let win = $(this); //this = window
        if (win.width() >= 769) { 
            $('.main-navigation ul').css( "display", "block" )
        }
        if (win.width() <= 768) { 
            $('.main-navigation ul').css( "display", "none" )
        }
  })



})