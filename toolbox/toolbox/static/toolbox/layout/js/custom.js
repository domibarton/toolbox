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

    /*
     * Add datepicker to date input fields.
     */

    $('input.dateinput').datepicker({
        autoclose: false,
        format: 'dd.mm.yyyy',
        language: 'en-GB',
        // startView: 'decade',
    });

    /*
     * Let's handle all generic HTML select dropdowns and convert them to nice
     * looking select2 dropdowns. Unfortunately, we need to handle also the
     * floating label thingy of the material design, so we need a bit of a hack
     * there as well.
     */

    // Replace the "empty" option with an empty string (instead of -----).
    $('select option').each(function(k,o)
    {
        if(o.value == '')
            o.innerHTML = '';
    });

});