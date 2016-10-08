/**
 * Created by Ben Maddison on 10/8/2016.
 */
$(document).ready( function () {
    var summary = $.getJSON("/api/session/status_summary/");
    var changed_sessions_table = $("#changed-sessions-table");
    changed_sessions_table.DataTable({
        processing: true,
        serverSide: true,
        ajax: "api/session/state_changes",
        searching: false,
        ordering: false,
        lengthChange: false,
        pageLength: 10,
        responsive: true,
        columns: [
            {title: "Previous", data: 'previous_state'},
            {title: "Current", data: 'session_state'},
            {title: "Peer", data: 'remote_network_name'},
            {title: "Address Family", data: 'address_family'},
            {title: "IXP", data: 'ixp_name'}
        ],
        rowCallback: function (row, data, index) {
            if (data.session_class) {
                $( row ).addClass(data.session_class);
            }
        }
    });
    var classes = {
        'Provisioning': "#2d9bd2",
        'Admin Down': "#e8c517",
        'Down': "#b84747",
        'Up': "#67b847"
    };
    var margin = 30;
    var layout = {
        margin: {t: margin, b: margin, l: margin, r: margin}
    };
    var pie = Plotly.d3.select('#pie').node();
    summary.done( function (response) {
        var values = [];
        var labels = [];
        var colors = [];
        for (i in response) {
            var label = response[i].label;
            if (label != "None") {
                labels.push(label);
                values.push(response[i].value);
                colors.push(classes[label]);
            }
        }
        var data = {
            showlegend: false,
            hole: 0.2,
            marker: {
                colors: colors,
                line: {color: "#fff" ,width: 2}
            },
            values: values,
            labels: labels,
            textinfo: "value",
            type: 'pie'
        };
        Plotly.newPlot(pie, [data], layout);
    });
})
