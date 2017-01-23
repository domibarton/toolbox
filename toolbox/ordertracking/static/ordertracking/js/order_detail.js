$(document).ready(function()
{
    $('table.order-list tbody td.id a').click(function(e)
    {
        e.preventDefault();

        var order_id = $(this).text();
        var url      = $(this).data('modal-url');
        var modal    = $('#detail');
        var title    = modal.find('.modal-title');
        var body     = modal.find('.modal-body');

        $.ajax(url).done(function(data)
        {
            title.text('Order ' + order_id);
            body.html(data);
            modal.modal('show');
        });

    });
});