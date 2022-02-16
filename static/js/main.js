
$(document).ready(function() {
    // NAVBAR SHRINK
    $(window).on("scroll",function(){
        if($(this).scrollTop() > 90){
         $(".navbar").addClass("navbar-shrink");
        }
        else{
            $(".navbar").removeClass("navbar-shrink");
        }      
    });

    // FEATURES CAROUSEL
    $('.features-carousel').owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            1000:{
                items:3,
            }
        }
    });

    // PAGE SCROLL
    $.scrollIt({
         topOffset: -50
    });

    //ABOUT-ITEM ANIMATE
    let nCount = selector => {
        $(selector).each(function () {
          $(this)
            .animate({
              Counter: $(this).text()
            }, {
              // A string or number determining how long the animation will run.
              duration: 4000,
              // A string indicating which easing function to use for the transition.
              easing: "swing",
              /**
               * A function to be called for each animated property of each animated element. 
               * This function provides an opportunity to
               *  modify the Tween object to change the value of the property before it is set.
               */
              step: function (value) {
                $(this).text(Math.ceil(value));
              }
            });
        });
      };
      
      let a = 0;
      $(window).scroll(function () {
        // The .offset() method allows us to retrieve the current position of an element  relative to the document
        let oTop = $(".about").offset().top - window.innerHeight;
        if (a == 0 && $(window).scrollTop() >= oTop) {
          a++;
          nCount(".about-item > h3");
        }
      });

       // FEATURES CAROUSEL
    $('.team-carousel').owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            1000:{
                items:3,
            }
        }
    });


    // ROOMS CAROUSEL
    $('.room-carousel').owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            1000:{
                items:3,
            }
        }
    });

});
