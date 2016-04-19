$(document).ready(function()
{
    /*
     * All the tables should be data tables.
     */

    $('table').dataTable({
        'pageLength': 100,
        'search': {
            'regex': true
        },
        'ordering': false
    });
});