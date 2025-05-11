$(document).ready(function() {

    $('.quiz-option').click(function() {
        var answer = $(this).data('index');
        var questionId = $(this).closest('.quiz-container').data('question-id');
        var nextUrl = $(this).closest('.quiz-container').data('next-url');
        

        $.ajax({
            url: '/quiz/' + questionId,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({answer: answer}),
            success: function(response) {
                if (response.success) {
                    window.location.href = nextUrl;
                } else {
                    alert('Failed to save your answer. Please try again.');
                }
            },
            error: function() {
                alert('Error submitting your answer. Please try again.');
            }
        });
    });
});