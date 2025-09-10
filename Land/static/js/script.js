$(document).ready(function(){
  $(".owl-carousel").owlCarousel({
    items:5,
    loop:true,
    margin:10,
    nav:false,
    dots:false,
    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:true
  });
});



  $('.carousel').carousel()
    $(document).ready(function(){
      $(".blog-carousel, .video-carousel, .event-carousel").owlCarousel({
          items: 1,               // show 1 item at a time
          loop: true,             // infinite loop
          margin: 10,
          autoplay: true,
          autoplayTimeout: 3000,
          autoplayHoverPause: true,
          animateOut: 'slideOutUp',
          animateIn: 'slideInUp',
          nav: true,
          dots: false
      });
    });