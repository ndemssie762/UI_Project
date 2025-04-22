$(document).ready(function() {
    // Quiz answer selection and submission
    $('.quiz-option').click(function() {
        var answer = $(this).data('index');
        var questionId = $(this).closest('.quiz-container').data('question-id');
        var nextUrl = $(this).closest('.quiz-container').data('next-url');
        $.ajax({
            url: '/quiz/' + questionId,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({answer: answer}),
            success: function() {
                window.location.href = nextUrl;
            }
        });
    });
});
