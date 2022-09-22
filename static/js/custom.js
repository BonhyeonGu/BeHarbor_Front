AOS.init({
	duration: 800,
	easing: 'slide',
	once: true
});

$(function(){

	'use strict';

	$(".loader").delay(500).fadeOut("slow");
	$("#overlayer").delay(500).fadeOut("slow");	

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
			$('.site-mobile-menu .has-children').each(function(){
				var $this = $(this);

				$this.prepend('<span class="arrow-collapse collapsed">');

				$this.find('.arrow-collapse').attr({
					'data-toggle' : 'collapse',
					'data-target' : '#collapseItem' + counter,
				});

				$this.find('> ul').attr({
					'class' : 'collapse',
					'id' : 'collapseItem' + counter,
				});

				counter++;

			});

		}, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
			var $this = $(this);
			if ( $this.closest('li').find('.collapse').hasClass('show') ) {
				$this.removeClass('active');
			} else {
				$this.addClass('active');
			}
			e.preventDefault();  

		});

		$(window).resize(function() {
			var $this = $(this),
			w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$('body').find('.js-menu-toggle').removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$('body').find('.js-menu-toggle').addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
			var container = $(".site-mobile-menu");
			if (!container.is(e.target) && container.has(e.target).length === 0) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
					$('body').find('.js-menu-toggle').removeClass('active');
				}
			}
		});
	}; 
	siteMenuClone();

	var owlPlugin = function() {
		if ( $('.owl-single').length > 0 ) {
			var owl = $('.owl-single').owlCarousel({
				loop: true,
				autoHeight: true,
				margin: 0,
				autoplay: true,
				smartSpeed: 1000,
				items: 1,
				nav: true,
				navText: ['<span class="icon-keyboard_backspace"></span>','<span class="icon-keyboard_backspace"></span>']
			});

			owl.on('initialized.owl.carousel', function() {
				owl.trigger('refresh.owl.carousel');
			});

			$('.custom-owl-next').click(function(e) {
				e.preventDefault();
				owl.trigger('next.owl.carousel');
			})
			$('.custom-owl-prev').click(function(e) {
				e.preventDefault();
				owl.trigger('prev.owl.carousel');
			})
		}


		if ( $('.owl-logos').length > 0 ) {
			var owl3 = $('.owl-logos').owlCarousel({
				loop: true,
				autoHeight: true,
				margin: 10,
				autoplay: true,
				smartSpeed: 700,
				items: 4,
				stagePadding: 0,
				nav: true,
				dots: true,
				navText: ['<span class="icon-keyboard_backspace"></span>','<span class="icon-keyboard_backspace"></span>'],
				responsive:{
					0:{
						items:1
					},
					600:{
						items:1
					},
					800: {
						items:2
					},
					1000:{
						items:3
					},
					1100:{
						items:5
					}
				}
			});
		}
		
		if ( $('.owl-3-slider').length > 0 ) {
			var owl3 = $('.owl-3-slider').owlCarousel({
				loop: true,
				autoHeight: true,
				margin: 10,
				autoplay: true,
				smartSpeed: 700,
				items: 4,
				stagePadding: 0,
				nav: true,
				dots: true,
				navText: ['<span class="icon-keyboard_backspace"></span>','<span class="icon-keyboard_backspace"></span>'],
				responsive:{
					0:{
						items:1
					},
					600:{
						items:1
					},
					800: {
						items:2
					},
					1000:{
						items:2
					},
					1100:{
						items:3
					}
				}
			});
		}
		




		if ( $('.owl-4-slider').length > 0 ) {
			var owl4 = $('.owl-4-slider').owlCarousel({
				loop: true,
				autoHeight: true,
				margin: 10,
				autoplay: true,
				smartSpeed: 1200,
				items: 1,
				nav: false,
				navText: ['<span class="icon-keyboard_backspace"></span>','<span class="icon-keyboard_backspace"></span>'],
				responsive:{
					0:{
						items:1
					},
					600:{
						items:2
					},
					1000:{
						items:4
					}
				}
			});

			$('.js-custom-next-v2').click(function(e) {
				e.preventDefault();
				owl4.trigger('next.owl.carousel');
			})
			$('.js-custom-prev-v2').click(function(e) {
				e.preventDefault();
				owl4.trigger('prev.owl.carousel');
			})
		}





		if ( $('.owl-single-text').length > 0 ) {
			var owlText = $('.owl-single-text').owlCarousel({
				loop: true,
				autoHeight: true,
				margin: 0,

				animateOut: 'fadeOut',
				animateIn: 'fadeIn',
				
				autoplay: true,
				smartSpeed: 1200,
				items: 1,
				nav: false,
				navText: ['<span class="icon-keyboard_backspace"></span>','<span class="icon-keyboard_backspace"></span>']
			});
		}
		if ( $('.owl-single-2').length > 0 ) {
			var owl = $('.owl-single-2').owlCarousel({
				loop: true,
				autoHeight: true,
				margin: 0,
				autoplay: true,
				smartSpeed: 800,
				items: 1,
				nav: false,
				navText: ['<span class="icon-keyboard_backspace"></span>','<span class="icon-keyboard_backspace"></span>'],
				onInitialized: counter
			});

			function counter(event) {
				$('.owl-total').text(event.item.count);
			}
			
			$('.js-custom-owl-next').click(function(e) {
				e.preventDefault();
				owl.trigger('next.owl.carousel');
				owlText.trigger('next.owl.carousel');
			})
			$('.js-custom-owl-prev').click(function(e) {
				e.preventDefault();
				owl.trigger('prev.owl.carousel');
				owlText.trigger('prev.owl.carousel');
			})

			$('.owl-dots .owl-dot').each(function(i) {
				$(this).attr('data-index', i - 3);
			});

			owl.on('changed.owl.carousel', function(event) {
				var i = event.item.index;
				if ( i === 1 ) {
					i = event.item.count;
				} else {
					i = i - 1;
				}
				$('.owl-current').text(i);
				$('.owl-total').text(event.item.count);
			})
		}
	}
	owlPlugin();

	var counter = function() {
		
		$('.count-numbers').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('ut-animated') ) {

				var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
				$('.counter > span').each(function(){
					var $this = $(this),
					num = $this.data('number');
					$this.animateNumber(
					{
						number: num,
						numberStep: comma_separator_number_step
					}, 10000,
					function() {
			      // $('.counter-caption').addClass('active')
			    }
			    );
				});
				
			}

		} , { offset: '95%' } );

	}
	counter();

	var portfolioMasonry = function() {
		$('.filters ul li').click(function(){
			$('.filters ul li').removeClass('active');
			$(this).addClass('active');
			
			var data = $(this).attr('data-filter');
			$grid.isotope({
				filter: data
			})
		});


		if(document.getElementById("portfolio-section")){
			var $grid = $(".grid").isotope({
				itemSelector: ".all",
				percentPosition: true,
				masonry: {
					columnWidth: ".all"
				}
			})

			$grid.imagesLoaded().progress( function() {
				$grid.isotope('layout');
			});  
			
		};


	};
	portfolioMasonry();

	$('.js-search-toggle').on('click', function() {
		$('.search-wrap').toggleClass('active');

		setTimeout(function() {
			$('#s').focus();
		}, 400);
	})

	$(document).mouseup(function(e) {
		var container = $(".search-wrap form");
		if (!container.is(e.target) && container.has(e.target).length === 0) {
			if ( $('.search-wrap').hasClass('active') ) {
				$('.search-wrap').removeClass('active');
			}
		}
	}); 

	var siteStellar = function() {
		$(window).stellar({
			responsive: false,
			parallaxBackgrounds: true,
			parallaxElements: true,
			horizontalScrolling: false,
			hideDistantElements: false,
			scrollProperty: 'scroll'
		});
	};
	siteStellar();

	var letteringPlugin = function() {
		$('.hero-heading').lettering('words');
		setTimeout(function() {
			$('.hero-heading > span > span').lettering('letters');
		}, 200)
	};
	letteringPlugin();

	var headingAnimate = function() {
		var tl = new TimelineMax();

		setTimeout(function() {
			tl 
			.set('.hero-heading > span > span > span > span', {y: "100%", transformStyle:"preserve-3d"})
			.set('.sub-text, .js-line', {y: 20, autoAlpha: 0, transformStyle:"preserve-3d"})
			.staggerFromTo('.hero-heading > span > span > span > span', 2, {opacity: 1, rotation: "20%", y:"100%"}, {opacity: 1, rotation: 0, y: "0%", ease: Expo.easeInOut}, 0.03, '+=0')
			.fromTo('.sub-text, .js-line', 1, { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, ease: Expo.easeInOut }, '-=1')
		}, 300);
	};
	headingAnimate();

	var pricing = function() {
		$('.js-period-toggle').on('click', function(e) {
			var $this = $(this),
			pricingItem = $('.pricing-item');
			if ( $('.period-toggle').hasClass('active') ) {
				$this.removeClass('active');
				pricingItem.removeClass('yearly');
			} else {
				$this.addClass('active');
				pricingItem.addClass('yearly');
			}
			e.preventDefault();
		})
	}
	pricing();

})