var chart;

$.getJSON('/standings_json').done(function(data) {


    var user_team = {};
    var data_var = [];
    var lbls = [];
    data.forEach(function(e) {
        lbls.push(e.TeamName);
          data_var[e.TeamName] = e.TeamPoints;

        if (e.UserTeam === 1) {
            user_team[e.TeamName] = e.TeamPoints
        }
    });

    chart = c3.generate({
        data: {
            json: data,
            keys: {
                x: "TeamName",
                value: ['TeamPoints']
            },
            type: 'spline',
        },
        axis: {
            x: {
                type: 'category',
                show: false,
                // categories: ["TeamName"],
                tick: {
                    rotate: (90),
                    // show: false,
                    // values: ["TeamName"],
                }
            }
        },
        // size: {
        //     height: 600
        // },
        legend: {
            show: false,
        },
        onresize: function(e) {
            if (this.width > 500) {

            }
            else {

            }

            chart.resize();
        }

    })
});


