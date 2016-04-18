$(document).ready(function()
{
    $('table').dataTable({
        'pageLength': 100,
        'search': {
            'regex': true
        },
        'ordering': false
    });
});