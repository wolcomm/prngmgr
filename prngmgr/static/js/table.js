$(document).ready(function () {
    var table = $('#data-table');
    var data_table;
    var table_def_src = table.attr("prngmgr-def-src");
    var table_data_src = table.attr("prngmgr-data-src");
    var table_def_query = $.getJSON(table_def_src);
    table_def_query.done( function (table_def) {
        data_table = table.DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": table_data_src,
            "searching": true,
            "pageLength": 25,
            "columns": table_def,
            "responsive": true,
            "drawCallback": function ( settings ) {
                data_table.responsive.recalc();
            },
            "rowCallback": function (row, data, index) {
                if (data.session_class) {
                    $( row ).addClass(data.session_class);
                }
            }
        })
    });
});
