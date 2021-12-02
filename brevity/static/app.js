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
    
});