$(document).ready(function() {

    $(document).on('click', '.upvote', function() {
        var post_id = $(this).attr('post_id');
        
        req = $.ajax({
            url : '/post/' + post_id + '/vote/upvote',
            type : 'POST',
            // data : { post_id : post_id, action : action}
        });

        req.done(function(data) {
            // $('#upvote'+post_id).fadeOut(1000).fadeIn(1000);
            // $('#memberSection'+member_id).fadeOut(1000).fadeIn(1000);
            $('#upvote'+post_id).text('(' + data.upvote_count + ')');
            $('#downvote'+post_id).text('(' + data.downvote_count + ')');
        });
    
    });


    $(document).on('click', '.downvote', function() {
        var post_id = $(this).attr('post_id');

        req = $.ajax({
            url : '/post/' + post_id + '/vote/downvote',
            type : 'POST',
            // data : { post_id : post_id, action : action}
        });

        req.done(function(data) {
            // $('#memberSection'+member_id).fadeOut(1000).fadeIn(1000);
            // $('#memberSection'+member_id).fadeOut(1000).fadeIn(1000);
            $('#downvote'+post_id).text('(' + data.downvote_count + ')');
            $('#upvote'+post_id).text('(' + data.upvote_count + ')');
        });
    });

    
});