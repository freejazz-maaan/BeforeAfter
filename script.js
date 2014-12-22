<script>
var outer = $('#slideshow');
var inners = $('.inner-slideshow');
var output = $('#output');

inners.on( 'cycle-finished', function( e, opts, curr, next ) {
    setTimeout(function() {
        outer.cycle( 'next' );
    }, 2500);
});

$('#slideshow').on( 'cycle-before', function( e, opts, curr, next ) {
    // ignore bubbled events from inner slideshows
    if (e.target !== this)
        return;

    //inners.cycle('stop');

    var index = opts.slides.index( next );
    output.html( 'starting slideshow #' + (index+1) );

    // start the next slideshow
    $( next ).find('.inner-slideshow').cycle('destroy').cycle({
        timeout: 2500
    });
});

</script>
