(function(global, factory) {
    // universal module definition
    /* jshint strict: false */
    /* globals define, module, window */
    if (typeof define == 'function' && define.amd) {
        // AMD - RequireJS
        define('ev-emitter/ev-emitter', factory);
    } else if (typeof module == 'object' && module.exports) {
        // CommonJS - Browserify, Webpack
        module.exports = factory();
    } else {
        // Browser globals
        global.EvEmitter = factory();
    }

}(typeof window != 'undefined' ? window : this, function() {



    function EvEmitter() {}

    var proto = EvEmitter.prototype;

    proto.on = function(eventName, listener) {
        if (!eventName || !listener) {
            return;
        }
        // set events hash
        var events = this._events = this._events || {};
        // set listeners array
        var listeners = events[eventName] = events[eventName] || [];
        // only add once
        if (listeners.indexOf(listener) == -1) {
            listeners.push(listener);
        }

        return this;
    };

    proto.once = function(eventName, listener) {
        if (!eventName || !listener) {
            return;
        }
        // add event
        this.on(eventName, listener);
        // set once flag
        // set onceEvents hash
        var onceEvents = this._onceEvents = this._onceEvents || {};
        // set onceListeners object
        var onceListeners = onceEvents[eventName] = onceEvents[eventName] || {};
        // set flag
        onceListeners[listener] = true;

        return this;
    };

    proto.off = function(eventName, listener) {
        var listeners = this._events && this._events[eventName];
        if (!listeners || !listeners.length) {
            return;
        }
        var index = listeners.indexOf(listener);
        if (index != -1) {
            listeners.splice(index, 1);
        }

        return this;
    };

    proto.emitEvent = function(eventName, args) {
        var listeners = this._events && this._events[eventName];
        if (!listeners || !listeners.length) {
            return;
        }
        // copy over to avoid interference if .off() in listener
        listeners = listeners.slice(0);
        args = args || [];
        // once stuff
        var onceListeners = this._onceEvents && this._onceEvents[eventName];

        for (var i = 0; i < listeners.length; i++) {
            var listener = listeners[i]
            var isOnce = onceListeners && onceListeners[listener];
            if (isOnce) {
                // remove listener
                // remove before trigger to prevent recursion
                this.off(eventName, listener);
                // unset once flag
                delete onceListeners[listener];
            }
            // trigger listener
            listener.apply(this, args);
        }

        return this;
    };

    proto.allOff = function() {
        delete this._events;
        delete this._onceEvents;
    };

    return EvEmitter;

}));

(function(window, factory) {
    'use strict';
    // universal module definition

    /*global define: false, module: false, require: false */

    if (typeof define == 'function' && define.amd) {
        // AMD
        define([
            'ev-emitter/ev-emitter'
        ], function(EvEmitter) {
            return factory(window, EvEmitter);
        });
    } else if (typeof module == 'object' && module.exports) {
        // CommonJS
        module.exports = factory(
            window,
            require('ev-emitter')
        );
    } else {
        // browser global
        window.imagesLoaded = factory(
            window,
            window.EvEmitter
        );
    }

})(typeof window !== 'undefined' ? window : this,

    // --------------------------  factory -------------------------- //

    function factory(window, EvEmitter) {



        var $ = window.jQuery;
        var console = window.console;

        // -------------------------- helpers -------------------------- //

        // extend objects
        function extend(a, b) {
            for (var prop in b) {
                a[prop] = b[prop];
            }
            return a;
        }

        var arraySlice = Array.prototype.slice;

        // turn element or nodeList into an array
        function makeArray(obj) {
            if (Array.isArray(obj)) {
                // use object if already an array
                return obj;
            }

            var isArrayLike = typeof obj == 'object' && typeof obj.length == 'number';
            if (isArrayLike) {
                // convert nodeList to array
                return arraySlice.call(obj);
            }

            // array of single index
            return [obj];
        }

        // -------------------------- imagesLoaded -------------------------- //

        /**
         * @param {Array, Element, NodeList, String} elem
         * @param {Object or Function} options - if function, use as callback
         * @param {Function} onAlways - callback function
         */
        function ImagesLoaded(elem, options, onAlways) {
            // coerce ImagesLoaded() without new, to be new ImagesLoaded()
            if (!(this instanceof ImagesLoaded)) {
                return new ImagesLoaded(elem, options, onAlways);
            }
            // use elem as selector string
            var queryElem = elem;
            if (typeof elem == 'string') {
                queryElem = document.querySelectorAll(elem);
            }
            // bail if bad element
            if (!queryElem) {
                console.error('Bad element for imagesLoaded ' + (queryElem || elem));
                return;
            }

            this.elements = makeArray(queryElem);
            this.options = extend({}, this.options);
            // shift arguments if no options set
            if (typeof options == 'function') {
                onAlways = options;
            } else {
                extend(this.options, options);
            }

            if (onAlways) {
                this.on('always', onAlways);
            }

            this.getImages();

            if ($) {
                // add jQuery Deferred object
                this.jqDeferred = new $.Deferred();
            }

            // HACK check async to allow time to bind listeners
            setTimeout(this.check.bind(this));
        }

        ImagesLoaded.prototype = Object.create(EvEmitter.prototype);

        ImagesLoaded.prototype.options = {};

        ImagesLoaded.prototype.getImages = function() {
            this.images = [];

            // filter & find items if we have an item selector
            this.elements.forEach(this.addElementImages, this);
        };

        /**
         * @param {Node} element
         */
        ImagesLoaded.prototype.addElementImages = function(elem) {
            // filter siblings
            if (elem.nodeName == 'IMG') {
                this.addImage(elem);
            }
            // get background image on element
            if (this.options.background === true) {
                this.addElementBackgroundImages(elem);
            }

            // find children
            // no non-element nodes, #143
            var nodeType = elem.nodeType;
            if (!nodeType || !elementNodeTypes[nodeType]) {
                return;
            }
            var childImgs = elem.querySelectorAll('img');
            // concat childElems to filterFound array
            for (var i = 0; i < childImgs.length; i++) {
                var img = childImgs[i];
                this.addImage(img);
            }

            // get child background images
            if (typeof this.options.background == 'string') {
                var children = elem.querySelectorAll(this.options.background);
                for (i = 0; i < children.length; i++) {
                    var child = children[i];
                    this.addElementBackgroundImages(child);
                }
            }
        };

        var elementNodeTypes = {
            1: true,
            9: true,
            11: true
        };

        ImagesLoaded.prototype.addElementBackgroundImages = function(elem) {
            var style = getComputedStyle(elem);
            if (!style) {
                // Firefox returns null if in a hidden iframe https://bugzil.la/548397
                return;
            }
            // get url inside url("...")
            var reURL = /url\((['"])?(.*?)\1\)/gi;
            var matches = reURL.exec(style.backgroundImage);
            while (matches !== null) {
                var url = matches && matches[2];
                if (url) {
                    this.addBackground(url, elem);
                }
                matches = reURL.exec(style.backgroundImage);
            }
        };

        /**
         * @param {Image} img
         */
        ImagesLoaded.prototype.addImage = function(img) {
            var loadingImage = new LoadingImage(img);
            this.images.push(loadingImage);
        };

        ImagesLoaded.prototype.addBackground = function(url, elem) {
            var background = new Background(url, elem);
            this.images.push(background);
        };

        ImagesLoaded.prototype.check = function() {
            var _this = this;
            this.progressedCount = 0;
            this.hasAnyBroken = false;
            // complete if no images
            if (!this.images.length) {
                this.complete();
                return;
            }

            function onProgress(image, elem, message) {
                // HACK - Chrome triggers event before object properties have changed. #83
                setTimeout(function() {
                    _this.progress(image, elem, message);
                });
            }

            this.images.forEach(function(loadingImage) {
                loadingImage.once('progress', onProgress);
                loadingImage.check();
            });
        };

        ImagesLoaded.prototype.progress = function(image, elem, message) {
            this.progressedCount++;
            this.hasAnyBroken = this.hasAnyBroken || !image.isLoaded;
            // progress event
            this.emitEvent('progress', [this, image, elem]);
            if (this.jqDeferred && this.jqDeferred.notify) {
                this.jqDeferred.notify(this, image);
            }
            // check if completed
            if (this.progressedCount == this.images.length) {
                this.complete();
            }

            if (this.options.debug && console) {
                console.log('progress: ' + message, image, elem);
            }
        };

        ImagesLoaded.prototype.complete = function() {
            var eventName = this.hasAnyBroken ? 'fail' : 'done';
            this.isComplete = true;
            this.emitEvent(eventName, [this]);
            this.emitEvent('always', [this]);
            if (this.jqDeferred) {
                var jqMethod = this.hasAnyBroken ? 'reject' : 'resolve';
                this.jqDeferred[jqMethod](this);
            }
        };

        // --------------------------  -------------------------- //

        function LoadingImage(img) {
            this.img = img;
        }

        LoadingImage.prototype = Object.create(EvEmitter.prototype);

        LoadingImage.prototype.check = function() {
            // If complete is true and browser supports natural sizes,
            // try to check for image status manually.
            var isComplete = this.getIsImageComplete();
            if (isComplete) {
                // report based on naturalWidth
                this.confirm(this.img.naturalWidth !== 0, 'naturalWidth');
                return;
            }

            // If none of the checks above matched, simulate loading on detached element.
            this.proxyImage = new Image();
            this.proxyImage.addEventListener('load', this);
            this.proxyImage.addEventListener('error', this);
            // bind to image as well for Firefox. #191
            this.img.addEventListener('load', this);
            this.img.addEventListener('error', this);
            this.proxyImage.src = this.img.src;
        };

        LoadingImage.prototype.getIsImageComplete = function() {
            // check for non-zero, non-undefined naturalWidth
            // fixes Safari+InfiniteScroll+Masonry bug infinite-scroll#671
            return this.img.complete && this.img.naturalWidth;
        };

        LoadingImage.prototype.confirm = function(isLoaded, message) {
            this.isLoaded = isLoaded;
            this.emitEvent('progress', [this, this.img, message]);
        };

        // ----- events ----- //

        // trigger specified handler for event type
        LoadingImage.prototype.handleEvent = function(event) {
            var method = 'on' + event.type;
            if (this[method]) {
                this[method](event);
            }
        };

        LoadingImage.prototype.onload = function() {
            this.confirm(true, 'onload');
            this.unbindEvents();
        };

        LoadingImage.prototype.onerror = function() {
            this.confirm(false, 'onerror');
            this.unbindEvents();
        };

        LoadingImage.prototype.unbindEvents = function() {
            this.proxyImage.removeEventListener('load', this);
            this.proxyImage.removeEventListener('error', this);
            this.img.removeEventListener('load', this);
            this.img.removeEventListener('error', this);
        };

        // -------------------------- Background -------------------------- //

        function Background(url, element) {
            this.url = url;
            this.element = element;
            this.img = new Image();
        }

        // inherit LoadingImage prototype
        Background.prototype = Object.create(LoadingImage.prototype);

        Background.prototype.check = function() {
            this.img.addEventListener('load', this);
            this.img.addEventListener('error', this);
            this.img.src = this.url;
            // check if image is already complete
            var isComplete = this.getIsImageComplete();
            if (isComplete) {
                this.confirm(this.img.naturalWidth !== 0, 'naturalWidth');
                this.unbindEvents();
            }
        };

        Background.prototype.unbindEvents = function() {
            this.img.removeEventListener('load', this);
            this.img.removeEventListener('error', this);
        };

        Background.prototype.confirm = function(isLoaded, message) {
            this.isLoaded = isLoaded;
            this.emitEvent('progress', [this, this.element, message]);
        };

        // -------------------------- jQuery -------------------------- //

        ImagesLoaded.makeJQueryPlugin = function(jQuery) {
            jQuery = jQuery || window.jQuery;
            if (!jQuery) {
                return;
            }
            // set local variable
            $ = jQuery;
            // $().imagesLoaded()
            $.fn.imagesLoaded = function(options, callback) {
                var instance = new ImagesLoaded(this, options, callback);
                return instance.jqDeferred.promise($(this));
            };
        };
        // try making plugin
        ImagesLoaded.makeJQueryPlugin();

        // --------------------------  -------------------------- //

        return ImagesLoaded;

    });

    "use strict";
    $(document).ready(function() {
    
        $("select").niceSelect();
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            AOS Animation Activation
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        AOS.init();
        window.addEventListener("load", AOS.refresh);
        AOS.init({
            once: true
        })
    
        /*Mesonary active*/
    
    
        var $grid = $('.iso-grid-wrap');
        $grid.packery({
            // options
            itemSelector: '.isotope-item',
            // gutter: 15,
            resize: true
        });
        $grid.imagesLoaded().progress(function() {
            $grid.packery('layout');
        });
    
    
        var $gridMas = $('.iso-mas-grid-wrap');
        $gridMas.packery({
            // options
            itemSelector: '.isotope-mas-item',
            // gutter: 15,
            resize: true
        });
        $gridMas.imagesLoaded().progress(function() {
            $gridMas.packery('layout');
        });
    
    
        // filter functions
        var filterFns = {
            // show if number is greater than 50
            numberGreaterThan50: function() {
                var number = $(this).find('.number').text();
                return parseInt(number, 10) > 50;
            },
            // show if name ends with -ium
            ium: function() {
                var name = $(this).find('.name').text();
                return name.match(/ium$/);
            }
        };
    
        // bind filter button click
        $('#isotope-filters').on('click', 'a', function() {
            var filterValue = $(this).attr('data-filter');
            // use filterFn if matches value
            filterValue = filterFns[filterValue] || filterValue;
            $grid.isotope({
                filter: filterValue
            });
        });
        // bind filter button click
        $('#isotope-mas-filters').on('click', 'a', function() {
            var filterValue = $(this).attr('data-filter');
            // use filterFn if matches value
            filterValue = filterFns[filterValue] || filterValue;
            $gridMas.isotope({
                filter: filterValue
            });
        });
    
        // change is-checked class on buttons
        $('.isotope-nav').each(function(i, buttonGroup) {
            var $buttonGroup = $(buttonGroup);
            $buttonGroup.on('click', 'a', function() {
                $buttonGroup.find('.active').removeClass('active');
                $(this).addClass('active');
            });
        });
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
             Landing 2 Testimonial
         <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        if (jQuery(".testimonial-slider-l2-1").length > 0) {
            $('.testimonial-slider-l2-1').slick({
    
                slidesToShow: 3,
                slidesToScroll: 1,
                // autoplay: true,
                swipe: true,
                infinite: true,
                autoplaySpeed: 2000,
                appendArrows: '.l2-slider-arrow-1',
                prevArrow: $('.prevl2'),
                nextArrow: $('.nextl2'),
                responsive: [{
                        breakpoint: 1199,
                        settings: {
                            centerPadding: '10%',
                            slidesToShow: 2
                        }
                    },
                    {
                        breakpoint: 767,
                        settings: {
                            centerPadding: '20px',
                            slidesToShow: 1
                        }
                    }
    
                ]
            });
        }
    
    
        /*l2 Testimonial slider button active*/
    
        $(document).ready(function() {
            $('.l2-slider-arrow-1 i').click(function() {
                $('.l2-slider-arrow-1 i').removeClass("slick-active");
                $(this).addClass("slick-active");
            });
        });
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
            Landing 5 Product Slider
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        if (jQuery(".product-slider-l5").length > 0) {
            $('.product-slider-l5').slick({
    
                slidesToShow: 3,
                slidesToScroll: 1,
                // autoplay: true,
                swipe: true,
                infinite: true,
                autoplaySpeed: 2000,
                appendArrows: '.l5-product-slider',
                prevArrow: $('.prev5-1'),
                nextArrow: $('.next5-1'),
                responsive: [{
                        breakpoint: 1199,
                        settings: {
                            centerPadding: '10%',
                            slidesToShow: 2
                        }
                    },
                    {
                        breakpoint: 767,
                        settings: {
                            centerPadding: '20px',
                            slidesToShow: 1
                        }
                    }
    
                ]
            });
        }
    
    
        /* Landing 5 Product Slider button active*/
    
        $(document).ready(function() {
            $('.l5-product-slider i').click(function() {
                $('.l5-product-slider i').removeClass("slick-active");
                $(this).addClass("slick-active");
            });
        });
    
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
            Landing 7 Hero slider
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        if (jQuery(".hero-l7-slider").length > 0) {
            $('.hero-l7-slider').slick({
                //  autoplay: true,
                slidesToShow: 1,
                slidesToScroll: 1,
                dots: true,
                swipe: true,
                infinite: true,
                appendArrows: '.testimonial-one-button',
                prevArrow: '<button type="button" class="slick-prev"><i class="icon icon-minimal-left"></i></button>',
                nextArrow: '<button type="button" class="slick-next"><i class="icon icon-minimal-right"></i></button>',
                autoplaySpeed: 2000,
                responsive: [{
                        breakpoint: 1199,
                        settings: {
                            centerPadding: '10%',
                            slidesToShow: 1
                        }
                    },
                    {
                        breakpoint: 767,
                        settings: {
                            centerPadding: '20px',
                            slidesToShow: 1
                        }
                    }
    
                ]
            });
        }
    
    
    
    
    
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
              Counter Up Activation
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        $('.counter').counterUp({
            delay: 10,
            time: 2000
        });
    
    
    
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
               Sticky Header
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        window.onscroll = function() {
            scrollFunction();
        };
    
        function scrollFunction() {
            if (
                document.body.scrollTop > 50 ||
                document.documentElement.scrollTop > 50
            ) {
                $(".site-header--sticky").addClass("scrolling");
            } else {
                $(".site-header--sticky").removeClass("scrolling");
            }
            if (
                document.body.scrollTop > 700 ||
                document.documentElement.scrollTop > 700
            ) {
                $(".site-header--sticky.scrolling").addClass("reveal-header");
            } else {
                $(".site-header--sticky.scrolling").removeClass("reveal-header");
            }
        }
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
               Prcing Dynamic Script
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        $('#table-price-value .toggle-btn').on("click", function(e) {
            console.log($(e.target).parent().parent().hasClass("monthly-active"));
            $(e.target).toggleClass("clicked");
            if ($(e.target).parent().parent().hasClass("monthly-active")) {
                $(e.target).parent().parent().removeClass("monthly-active").addClass("yearly-active");
            } else {
                $(e.target).parent().parent().removeClass("yearly-active").addClass("monthly-active");
            }
        });
    
        $("[data-pricing-trigger]").on("click", function(e) {
            $(e.target).addClass("active").siblings().removeClass("active");
            var target = $(e.target).attr("data-target");
            console.log($(target).attr("data-value-active") == "monthly");
            if ($(target).attr("data-value-active") == "monthly") {
                $(target).attr("data-value-active", "yearly");
            } else {
                $(target).attr("data-value-active", "monthly");
            }
        });
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
               Smooth Scroll
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        $(".goto").on("click", function(event) {
            if (this.hash !== "") {
                event.preventDefault();
                var hash = this.hash;
                $("html, body").animate({
                        scrollTop: $(hash).offset().top,
                    },
                    2000,
                    function() {
                        window.location.hash = hash;
                    }
                );
            } // End if
        });
    
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
              Preloader Activation
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        $(window).load(function() {
            setTimeout(function() {
                $("#loading").fadeOut(500);
            }, 1000);
            setTimeout(function() {
                $("#loading").remove();
            }, 2000);
        });
    
    
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
              Home-2- testimonial  Slider Appex
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
        var slickContentslide = {
            infinite: true,
            speed: 300,
            slidesToShow: 1,
            asNavFor: '.l2-testimonial-image-slider',
            adaptiveHeight: false,
            prevArrow: $('.prev3'),
            nextArrow: $('.next3'),
            fade: true,
            cssEase: 'linear'
        }
    
        var slickImgslide2 = {
            infinite: true,
            speed: 300,
            slidesToShow: 1,
            adaptiveHeight: false,
            asNavFor: '.l2-testimonial-text-slider',
            prevArrow: $('.prev3'),
            nextArrow: $('.next3'),
            fade: true,
            cssEase: 'linear'
        }
    
    
        $('.l2-testimonial-image-slider').slick(slickImgslide2);
        $('.l2-testimonial-text-slider').slick(slickContentslide);
    
        /*l2 Testimonial slider button active*/
    
        $(document).ready(function() {
            $('.next-prev-btn3 span').click(function() {
                $('.next-prev-btn3 span').removeClass("active");
                $(this).addClass("active");
            });
        });
    
    
    
        /*----------------------------------------
                Accordian Plugin
            ----------------------------------------*/
    
        (function($) {
            $('.accordion > li:eq(0) a').addClass('active').next().slideDown();
    
            $('.accordion a').click(function(j) {
                var dropDown = $(this).closest('li').find('p');
    
                $(this).closest('.accordion').find('p').not(dropDown).slideUp();
    
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                } else {
                    $(this).closest('.accordion').find('a.active').removeClass('active');
                    $(this).addClass('active');
                }
    
                dropDown.stop(false, true).slideToggle();
    
                j.preventDefault();
            });
        })(jQuery);
    
    
        /*Accordian L-12 li active shade*/
    
        $(document).ready(function() {
            $('.faq-l-12-1 li').click(function() {
                $('.faq-l-12-1 li').removeClass("active");
                $(this).addClass("active");
            });
        });
    
    
        /*FAQ TAB li active*/
    
        $(document).ready(function() {
            $('.faq-main-tab-area li').click(function() {
                $('.faq-main-tab-area li').removeClass("active");
                $(this).addClass("active");
            });
        });
    
        /*Pagination active*/
    
        $(document).ready(function() {
            $('.shop-pagination a').click(function() {
                $('.shop-pagination a').removeClass("active");
                $(this).addClass("active");
            });
        });
    
    
        $(document).ready(function() {
            $('.blog-pagination a').click(function() {
                $('.blog-pagination a').removeClass("active");
                $(this).addClass("active");
            });
        });
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
              Landing 11 Testimonial Slider
          <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        if (jQuery(".testimonial-slider-l-11").length > 0) {
            $(".testimonial-slider-l-11").slick({
                dots: false,
                arrows: true,
                infinite: true,
                speed: 500,
                slidesToShow: 2,
                slidesToScroll: 2,
                prevArrow: '<div class="l-11-slide-btn slick-prev focus-reset"><img src="../image/l2/long-arrow-left.png" alt=""></div>',
                nextArrow: '<div class="l-11-slide-btn slick-next focus-reset"><img src="../image/l2/long-arrow-right.png" alt=""></div>',
                responsive: [{
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    },
                }, ],
            });
        }
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
             Landing 12 Testimonial Slider
         <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        if (jQuery(".testimonial-slider-l-12").length > 0) {
            $('.testimonial-slider-l-12').slick({
    
                slidesToShow: 3,
                slidesToScroll: 1,
                // autoplay: true,
                swipe: true,
                infinite: true,
                autoplaySpeed: 2000,
                appendArrows: '.l-12-slider-arrow-1',
                prevArrow: $('.prev9'),
                nextArrow: $('.next9'),
                responsive: [{
                        breakpoint: 1199,
                        settings: {
                            centerPadding: '10%',
                            slidesToShow: 2
                        }
                    },
                    {
                        breakpoint: 767,
                        settings: {
                            centerPadding: '20px',
                            slidesToShow: 1
                        }
                    }
    
                ]
            });
        }
    
        /*Landing 12 Testimonial slider arrow active*/
    
        $(document).ready(function() {
            $('.l-12-slider-arrow-1 i').click(function() {
                $('.l-12-slider-arrow-1 i').removeClass("slick-active");
                $(this).addClass("slick-active");
            });
        });
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
             Landing 16 Screenshot Slider
         <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        if (jQuery(".screenshot-slider").length > 0) {
    
            $('.screenshot-slider').slick({
                slidesToShow: 5,
                slidesToScroll: 1,
                dots: true,
                arrows: true,
                prevArrow: '<button class="l-16-slide-btn slick-prev focus-reset "><i class="icon icon-stre-right"></i></button>',
                nextArrow: '<button class="l-16-slide-btn active slick-next focus-reset"><i class="icon icon-stre-left"></i></button>',
                centerMode: true,
                centerPadding: '130px',
                autoplay: true,
                autoplaySpeed: 3000,
                infinite: true,
                easing: 'linear',
                speed: 800,
                appendDots: ".screenshots-dots-l-16",
                responsive: [{
                        breakpoint: 1800,
                        settings: {
                            slidesToShow: 5,
                            centerPadding: '100px',
    
                        }
                    },
                    {
                        breakpoint: 1750,
                        settings: {
                            slidesToShow: 5,
                            centerPadding: '20px',
    
                        }
                    },
                    {
                        breakpoint: 1670,
                        settings: {
                            slidesToShow: 4,
                            centerPadding: '60px',
    
                        }
                    },
                    {
                        breakpoint: 1640,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '20px',
    
                        }
                    },
                    {
                        breakpoint: 1550,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '30px',
    
                        }
                    },
                    {
                        breakpoint: 1450,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '10px',
    
                        }
                    },
                    {
                        breakpoint: 1350,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '20px',
    
                        }
                    },
                    {
                        breakpoint: 1250,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '10px',
    
                        }
                    },
                    {
                        breakpoint: 1150,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '0px',
    
                        }
                    },
                    {
                        breakpoint: 1050,
                        settings: {
                            slidesToShow: 3,
                            centerPadding: '10px',
    
                        }
                    },
                    {
                        breakpoint: 950,
                        settings: {
                            slidesToShow: 1,
                            centerPadding: '0',
    
                        }
                    },
                    {
                        breakpoint: 850,
                        settings: {
                            slidesToShow: 1,
                            centerPadding: '20px',
                        }
                    },
                    {
                        breakpoint: 750,
                        settings: {
                            slidesToShow: 1,
                            centerPadding: '20px',
                        }
                    },
                    {
                        breakpoint: 650,
                        settings: {
                            slidesToShow: 1,
                            centerPadding: '10px',
                        }
                    },
                    {
                        breakpoint: 515,
                        settings: {
                            slidesToShow: 1,
                            autoplay: true,
                            centerPadding: '0px',
                        }
                    },
                    {
                        breakpoint: 480,
                        settings: {
                            slidesToShow: 1,
                            autoplay: true,
                            centerPadding: '0px',
                            arrows: false,
                        }
                    }
    
                ]
            });
        }
    
        /*Landing L-16 slider arrow active*/
    
        $(document).ready(function() {
            $('.l-16-slide-btn').click(function() {
                $('.l-16-slide-btn').removeClass("active");
                $(this).addClass("active");
            });
        });
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
               Landing 16 testimonial Slider
           <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
    
        if (jQuery(".testimonial-slider-l-16").length > 0) {
            $(".testimonial-slider-l-16").slick({
                dots: false,
                arrows: true,
                infinite: true,
                speed: 500,
                slidesToShow: 2,
                slidesToScroll: 2,
                responsive: [{
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    },
                }, ],
            });
        }
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
                Landing 18 testimonial Slider
            <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        if (jQuery(".testimonial-card-slider-l-18").length > 0) {
            $(".testimonial-card-slider-l-18").slick({
                dots: true,
                arrows: false,
                infinite: true,
                speed: 500,
                slidesToShow: 1,
                slidesToScroll: 1,
                responsive: [{
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    },
                }, ],
            });
        }
    
    
        /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
             Product Details SLider portfolio-details-3
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    
        if (jQuery(".product-details-vertical-slider").length > 0) {
            $('.product-details-vertical-slider').slick({
                dots: false,
                infinite: true,
                speed: 500,
                slidesToShow: 3,
                slidesToScroll: 1,
                arrows: false,
                focusOnSelect: true,
                vertical: true,
                asNavFor: '.product-details-slider',
                responsive: [{
                        breakpoint: 768,
                        settings: {
                            vertical: false
                        }
                    },
                    {
                        breakpoint: 575,
                        settings: {
                            vertical: false
                        }
                    }
                ]
            });
        }
    
        if (jQuery(".product-details-slider").length > 0) {
            $('.product-details-slider').slick({
                dots: false,
                infinite: true,
                speed: 500,
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: true,
                asNavFor: '.product-details-vertical-slider'
            });
        }
    
    
    
    });

    ! function(e, t) {
        "object" == typeof exports && "object" == typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define([], t) : "object" == typeof exports ? exports.AOS = t() : e.AOS = t()
    }(this, function() {
        return function(e) {
            function t(o) {
                if (n[o]) return n[o].exports;
                var i = n[o] = {
                    exports: {},
                    id: o,
                    loaded: !1
                };
                return e[o].call(i.exports, i, i.exports, t), i.loaded = !0, i.exports
            }
            var n = {};
            return t.m = e, t.c = n, t.p = "dist/", t(0)
        }([function(e, t, n) {
            "use strict";
    
            function o(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }
            var i = Object.assign || function(e) {
                    for (var t = 1; t < arguments.length; t++) {
                        var n = arguments[t];
                        for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
                    }
                    return e
                },
                r = n(1),
                a = (o(r), n(6)),
                u = o(a),
                c = n(7),
                s = o(c),
                f = n(8),
                d = o(f),
                l = n(9),
                p = o(l),
                m = n(10),
                b = o(m),
                v = n(11),
                y = o(v),
                g = n(14),
                h = o(g),
                w = [],
                k = !1,
                x = {
                    offset: 120,
                    delay: 0,
                    easing: "ease",
                    duration: 400,
                    disable: !1,
                    once: !1,
                    startEvent: "DOMContentLoaded",
                    throttleDelay: 99,
                    debounceDelay: 50,
                    disableMutationObserver: !1
                },
                j = function() {
                    var e = arguments.length > 0 && void 0 !== arguments[0] && arguments[0];
                    if (e && (k = !0), k) return w = (0, y.default)(w, x), (0, b.default)(w, x.once), w
                },
                O = function() {
                    w = (0, h.default)(), j()
                },
                M = function() {
                    w.forEach(function(e, t) {
                        e.node.removeAttribute("data-aos"), e.node.removeAttribute("data-aos-easing"), e.node.removeAttribute("data-aos-duration"), e.node.removeAttribute("data-aos-delay")
                    })
                },
                S = function(e) {
                    return e === !0 || "mobile" === e && p.default.mobile() || "phone" === e && p.default.phone() || "tablet" === e && p.default.tablet() || "function" == typeof e && e() === !0
                },
                _ = function(e) {
                    x = i(x, e), w = (0, h.default)();
                    var t = document.all && !window.atob;
                    return S(x.disable) || t ? M() : (x.disableMutationObserver || d.default.isSupported() || (console.info('\n      aos: MutationObserver is not supported on this browser,\n      code mutations observing has been disabled.\n      You may have to call "refreshHard()" by yourself.\n    '), x.disableMutationObserver = !0), document.querySelector("body").setAttribute("data-aos-easing", x.easing), document.querySelector("body").setAttribute("data-aos-duration", x.duration), document.querySelector("body").setAttribute("data-aos-delay", x.delay), "DOMContentLoaded" === x.startEvent && ["complete", "interactive"].indexOf(document.readyState) > -1 ? j(!0) : "load" === x.startEvent ? window.addEventListener(x.startEvent, function() {
                        j(!0)
                    }) : document.addEventListener(x.startEvent, function() {
                        j(!0)
                    }), window.addEventListener("resize", (0, s.default)(j, x.debounceDelay, !0)), window.addEventListener("orientationchange", (0, s.default)(j, x.debounceDelay, !0)), window.addEventListener("scroll", (0, u.default)(function() {
                        (0, b.default)(w, x.once)
                    }, x.throttleDelay)), x.disableMutationObserver || d.default.ready("[data-aos]", O), w)
                };
            e.exports = {
                init: _,
                refresh: j,
                refreshHard: O
            }
        }, function(e, t) {}, , , , , function(e, t) {
            (function(t) {
                "use strict";
    
                function n(e, t, n) {
                    function o(t) {
                        var n = b,
                            o = v;
                        return b = v = void 0, k = t, g = e.apply(o, n)
                    }
    
                    function r(e) {
                        return k = e, h = setTimeout(f, t), M ? o(e) : g
                    }
    
                    function a(e) {
                        var n = e - w,
                            o = e - k,
                            i = t - n;
                        return S ? j(i, y - o) : i
                    }
    
                    function c(e) {
                        var n = e - w,
                            o = e - k;
                        return void 0 === w || n >= t || n < 0 || S && o >= y
                    }
    
                    function f() {
                        var e = O();
                        return c(e) ? d(e) : void(h = setTimeout(f, a(e)))
                    }
    
                    function d(e) {
                        return h = void 0, _ && b ? o(e) : (b = v = void 0, g)
                    }
    
                    function l() {
                        void 0 !== h && clearTimeout(h), k = 0, b = w = v = h = void 0
                    }
    
                    function p() {
                        return void 0 === h ? g : d(O())
                    }
    
                    function m() {
                        var e = O(),
                            n = c(e);
                        if (b = arguments, v = this, w = e, n) {
                            if (void 0 === h) return r(w);
                            if (S) return h = setTimeout(f, t), o(w)
                        }
                        return void 0 === h && (h = setTimeout(f, t)), g
                    }
                    var b, v, y, g, h, w, k = 0,
                        M = !1,
                        S = !1,
                        _ = !0;
                    if ("function" != typeof e) throw new TypeError(s);
                    return t = u(t) || 0, i(n) && (M = !!n.leading, S = "maxWait" in n, y = S ? x(u(n.maxWait) || 0, t) : y, _ = "trailing" in n ? !!n.trailing : _), m.cancel = l, m.flush = p, m
                }
    
                function o(e, t, o) {
                    var r = !0,
                        a = !0;
                    if ("function" != typeof e) throw new TypeError(s);
                    return i(o) && (r = "leading" in o ? !!o.leading : r, a = "trailing" in o ? !!o.trailing : a), n(e, t, {
                        leading: r,
                        maxWait: t,
                        trailing: a
                    })
                }
    
                function i(e) {
                    var t = "undefined" == typeof e ? "undefined" : c(e);
                    return !!e && ("object" == t || "function" == t)
                }
    
                function r(e) {
                    return !!e && "object" == ("undefined" == typeof e ? "undefined" : c(e))
                }
    
                function a(e) {
                    return "symbol" == ("undefined" == typeof e ? "undefined" : c(e)) || r(e) && k.call(e) == d
                }
    
                function u(e) {
                    if ("number" == typeof e) return e;
                    if (a(e)) return f;
                    if (i(e)) {
                        var t = "function" == typeof e.valueOf ? e.valueOf() : e;
                        e = i(t) ? t + "" : t
                    }
                    if ("string" != typeof e) return 0 === e ? e : +e;
                    e = e.replace(l, "");
                    var n = m.test(e);
                    return n || b.test(e) ? v(e.slice(2), n ? 2 : 8) : p.test(e) ? f : +e
                }
                var c = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
                        return typeof e
                    } : function(e) {
                        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
                    },
                    s = "Expected a function",
                    f = NaN,
                    d = "[object Symbol]",
                    l = /^\s+|\s+$/g,
                    p = /^[-+]0x[0-9a-f]+$/i,
                    m = /^0b[01]+$/i,
                    b = /^0o[0-7]+$/i,
                    v = parseInt,
                    y = "object" == ("undefined" == typeof t ? "undefined" : c(t)) && t && t.Object === Object && t,
                    g = "object" == ("undefined" == typeof self ? "undefined" : c(self)) && self && self.Object === Object && self,
                    h = y || g || Function("return this")(),
                    w = Object.prototype,
                    k = w.toString,
                    x = Math.max,
                    j = Math.min,
                    O = function() {
                        return h.Date.now()
                    };
                e.exports = o
            }).call(t, function() {
                return this
            }())
        }, function(e, t) {
            (function(t) {
                "use strict";
    
                function n(e, t, n) {
                    function i(t) {
                        var n = b,
                            o = v;
                        return b = v = void 0, O = t, g = e.apply(o, n)
                    }
    
                    function r(e) {
                        return O = e, h = setTimeout(f, t), M ? i(e) : g
                    }
    
                    function u(e) {
                        var n = e - w,
                            o = e - O,
                            i = t - n;
                        return S ? x(i, y - o) : i
                    }
    
                    function s(e) {
                        var n = e - w,
                            o = e - O;
                        return void 0 === w || n >= t || n < 0 || S && o >= y
                    }
    
                    function f() {
                        var e = j();
                        return s(e) ? d(e) : void(h = setTimeout(f, u(e)))
                    }
    
                    function d(e) {
                        return h = void 0, _ && b ? i(e) : (b = v = void 0, g)
                    }
    
                    function l() {
                        void 0 !== h && clearTimeout(h), O = 0, b = w = v = h = void 0
                    }
    
                    function p() {
                        return void 0 === h ? g : d(j())
                    }
    
                    function m() {
                        var e = j(),
                            n = s(e);
                        if (b = arguments, v = this, w = e, n) {
                            if (void 0 === h) return r(w);
                            if (S) return h = setTimeout(f, t), i(w)
                        }
                        return void 0 === h && (h = setTimeout(f, t)), g
                    }
                    var b, v, y, g, h, w, O = 0,
                        M = !1,
                        S = !1,
                        _ = !0;
                    if ("function" != typeof e) throw new TypeError(c);
                    return t = a(t) || 0, o(n) && (M = !!n.leading, S = "maxWait" in n, y = S ? k(a(n.maxWait) || 0, t) : y, _ = "trailing" in n ? !!n.trailing : _), m.cancel = l, m.flush = p, m
                }
    
                function o(e) {
                    var t = "undefined" == typeof e ? "undefined" : u(e);
                    return !!e && ("object" == t || "function" == t)
                }
    
                function i(e) {
                    return !!e && "object" == ("undefined" == typeof e ? "undefined" : u(e))
                }
    
                function r(e) {
                    return "symbol" == ("undefined" == typeof e ? "undefined" : u(e)) || i(e) && w.call(e) == f
                }
    
                function a(e) {
                    if ("number" == typeof e) return e;
                    if (r(e)) return s;
                    if (o(e)) {
                        var t = "function" == typeof e.valueOf ? e.valueOf() : e;
                        e = o(t) ? t + "" : t
                    }
                    if ("string" != typeof e) return 0 === e ? e : +e;
                    e = e.replace(d, "");
                    var n = p.test(e);
                    return n || m.test(e) ? b(e.slice(2), n ? 2 : 8) : l.test(e) ? s : +e
                }
                var u = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
                        return typeof e
                    } : function(e) {
                        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
                    },
                    c = "Expected a function",
                    s = NaN,
                    f = "[object Symbol]",
                    d = /^\s+|\s+$/g,
                    l = /^[-+]0x[0-9a-f]+$/i,
                    p = /^0b[01]+$/i,
                    m = /^0o[0-7]+$/i,
                    b = parseInt,
                    v = "object" == ("undefined" == typeof t ? "undefined" : u(t)) && t && t.Object === Object && t,
                    y = "object" == ("undefined" == typeof self ? "undefined" : u(self)) && self && self.Object === Object && self,
                    g = v || y || Function("return this")(),
                    h = Object.prototype,
                    w = h.toString,
                    k = Math.max,
                    x = Math.min,
                    j = function() {
                        return g.Date.now()
                    };
                e.exports = n
            }).call(t, function() {
                return this
            }())
        }, function(e, t) {
            "use strict";
    
            function n(e) {
                var t = void 0,
                    o = void 0,
                    i = void 0;
                for (t = 0; t < e.length; t += 1) {
                    if (o = e[t], o.dataset && o.dataset.aos) return !0;
                    if (i = o.children && n(o.children)) return !0
                }
                return !1
            }
    
            function o() {
                return window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver
            }
    
            function i() {
                return !!o()
            }
    
            function r(e, t) {
                var n = window.document,
                    i = o(),
                    r = new i(a);
                u = t, r.observe(n.documentElement, {
                    childList: !0,
                    subtree: !0,
                    removedNodes: !0
                })
            }
    
            function a(e) {
                e && e.forEach(function(e) {
                    var t = Array.prototype.slice.call(e.addedNodes),
                        o = Array.prototype.slice.call(e.removedNodes),
                        i = t.concat(o);
                    if (n(i)) return u()
                })
            }
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var u = function() {};
            t.default = {
                isSupported: i,
                ready: r
            }
        }, function(e, t) {
            "use strict";
    
            function n(e, t) {
                if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
            }
    
            function o() {
                return navigator.userAgent || navigator.vendor || window.opera || ""
            }
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var i = function() {
                    function e(e, t) {
                        for (var n = 0; n < t.length; n++) {
                            var o = t[n];
                            o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
                        }
                    }
                    return function(t, n, o) {
                        return n && e(t.prototype, n), o && e(t, o), t
                    }
                }(),
                r = /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i,
                a = /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i,
                u = /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i,
                c = /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i,
                s = function() {
                    function e() {
                        n(this, e)
                    }
                    return i(e, [{
                        key: "phone",
                        value: function() {
                            var e = o();
                            return !(!r.test(e) && !a.test(e.substr(0, 4)))
                        }
                    }, {
                        key: "mobile",
                        value: function() {
                            var e = o();
                            return !(!u.test(e) && !c.test(e.substr(0, 4)))
                        }
                    }, {
                        key: "tablet",
                        value: function() {
                            return this.mobile() && !this.phone()
                        }
                    }]), e
                }();
            t.default = new s
        }, function(e, t) {
            "use strict";
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var n = function(e, t, n) {
                    var o = e.node.getAttribute("data-aos-once");
                    t > e.position ? e.node.classList.add("aos-animate") : "undefined" != typeof o && ("false" === o || !n && "true" !== o) && e.node.classList.remove("aos-animate")
                },
                o = function(e, t) {
                    var o = window.pageYOffset,
                        i = window.innerHeight;
                    e.forEach(function(e, r) {
                        n(e, i + o, t)
                    })
                };
            t.default = o
        }, function(e, t, n) {
            "use strict";
    
            function o(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var i = n(12),
                r = o(i),
                a = function(e, t) {
                    return e.forEach(function(e, n) {
                        e.node.classList.add("aos-init"), e.position = (0, r.default)(e.node, t.offset)
                    }), e
                };
            t.default = a
        }, function(e, t, n) {
            "use strict";
    
            function o(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var i = n(13),
                r = o(i),
                a = function(e, t) {
                    var n = 0,
                        o = 0,
                        i = window.innerHeight,
                        a = {
                            offset: e.getAttribute("data-aos-offset"),
                            anchor: e.getAttribute("data-aos-anchor"),
                            anchorPlacement: e.getAttribute("data-aos-anchor-placement")
                        };
                    switch (a.offset && !isNaN(a.offset) && (o = parseInt(a.offset)), a.anchor && document.querySelectorAll(a.anchor) && (e = document.querySelectorAll(a.anchor)[0]), n = (0, r.default)(e).top, a.anchorPlacement) {
                        case "top-bottom":
                            break;
                        case "center-bottom":
                            n += e.offsetHeight / 2;
                            break;
                        case "bottom-bottom":
                            n += e.offsetHeight;
                            break;
                        case "top-center":
                            n += i / 2;
                            break;
                        case "bottom-center":
                            n += i / 2 + e.offsetHeight;
                            break;
                        case "center-center":
                            n += i / 2 + e.offsetHeight / 2;
                            break;
                        case "top-top":
                            n += i;
                            break;
                        case "bottom-top":
                            n += e.offsetHeight + i;
                            break;
                        case "center-top":
                            n += e.offsetHeight / 2 + i
                    }
                    return a.anchorPlacement || a.offset || isNaN(t) || (o = t), n + o
                };
            t.default = a
        }, function(e, t) {
            "use strict";
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var n = function(e) {
                for (var t = 0, n = 0; e && !isNaN(e.offsetLeft) && !isNaN(e.offsetTop);) t += e.offsetLeft - ("BODY" != e.tagName ? e.scrollLeft : 0), n += e.offsetTop - ("BODY" != e.tagName ? e.scrollTop : 0), e = e.offsetParent;
                return {
                    top: n,
                    left: t
                }
            };
            t.default = n
        }, function(e, t) {
            "use strict";
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            var n = function(e) {
                return e = e || document.querySelectorAll("[data-aos]"), Array.prototype.map.call(e, function(e) {
                    return {
                        node: e
                    }
                })
            };
            t.default = n
        }])
    });