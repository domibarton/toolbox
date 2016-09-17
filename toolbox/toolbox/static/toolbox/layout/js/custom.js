$(document).ready(function()
{
    /*
     * All the tables should be data tables.
     */

    tables = $('table');

    tables.DataTable({
        'pageLength': 100,
        'search': {
            'regex': true
        },
        'ordering': false
    });


    tables.DataTable().columns().every(function()
    {
        var that = this;
        $('input', this.header()).on('keyup change', function ()
        {
            if(that.search() !== this.value)
                that.search(this.value).draw();
        });
    });

});