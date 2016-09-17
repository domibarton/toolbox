$(document).ready(function()
{
    $('table#orderlist tbody td.id a').click(function(e)
    {
        e.preventDefault();

        var link  = $(this);
        var modal = $('#detail');
        var title = modal.find('.modal-title');
        var body  = modal.find('.modal-body');

        $.ajax(link.attr('href')).done(function(data)
        {
            title.text('Order ' + link.text());
            body.html(data);
            modal.modal('show');
        });

    });
});