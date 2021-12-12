$(document).ready(function() {

    $(document).on('click', '.vote', function() {
        var post_id = $(this).attr('post_id');
        var action = $(this).attr('action');
        
        req = $.ajax({
            url : '/post/' + post_id + '/vote/' + action,
            type : 'POST',
            // data : { post_id : post_id, action : action}
        });

        req.done(function(data) {
            // $('#upvote'+post_id).fadeOut(1000).fadeIn(1000);
            // $('#memberSection'+member_id).fadeOut(1000).fadeIn(1000);
            $('#vote'+post_id).html(data);
        });
    
    });

    var timer = null;
    var xhr = null;
    $('.user_popup').hover(
        function(event) {
            // mouse in event handler
            
            var elem = $(event.currentTarget);
            timer = setTimeout(function() {
                timer = null;
                xhr = $.ajax(
                    '/user/' + elem.first().text().trim() + '/popup').done(
                        function(data) {
                            xhr = null;
                            elem.popover({
                                trigger: 'manual',
                                html: true,
                                animation: true,
                                container: elem,
                                content: data
                            }).popover('show');
                            
                        }
                    );
            }, 500);
        },
        function(event) {
            // mouse out event handler
            
            var elem = $(event.currentTarget);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            else if (xhr) {
                xhr.abort();
                xhr = null;
            }
            else {
                $('.popover').remove();
            }
        }
    );

});



