var base_url = location["protocol"] + "//" + location["host"] + "/";
var standings_api = base_url + "api" + "/";
var current_standings_url = standings_api + "standings/";
var all_standings_url = standings_api + "/all_standings/";

var colors = [
    '#FF6666',
    '#FFB266',
    '#FFFF66',
    '#B2FF66',
    '#66FF66',
    '#66FFB2',
    '#66FFFF',
    '#66B2FF',
    '#6666FF',
    '#B266FF',
    '#FF66FF',
    '#FF66B2'
];

var standings_data;
function get_standings() {
    $.getJSON(
        current_standings_url + "?format=json", function(data) {
            standings_data = process_data(data);
            create_chart();
        }
    )
}

function get_all_standings() {
    $.getJSON(
        all_standings_url + "?format=json", function(data) {
            standings_data = process_data(data);
        }
    )
}


function process_data(data) {
    var dt = [];
    var lbl = [];
    for (var i=0; i < data.length; i++) {
        var current_team = data[i];
        // dt.push({
        //     'x': current_team['team']['team_name'],
        //     'y': current_team["stat_point_total"]
        // });
        lbl.push(current_team['team']['team_name']);
        dt.push(current_team['stat_point_total'])
    }
    var out_data = {
        labels: lbl,
        datasets: [{
            data: dt,
            backgroundColor: colors
        }],
    };
    return out_data;
}


var myChart;
function create_chart() {
    var ctx = document.getElementById("myChart");

    myChart = new Chart(ctx, {
        type: 'bar',
        data: standings_data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    maxBarThickness: 50,
                    ticks: {
                        autoSkip: false
                    }
                    }],
            },
            legend: {
                display: false
            },
        }
    },);
}

function check_chart_hidden() {
    var hidden = $(".canvas_column").attr('hidden');
    if (hidden === 'hidden') {
        return false;
    }
    else {
        return true;
    }
}

function hide_chart() {
    $(".land_view").attr('hidden', '');
    $(".port_view").removeAttr('hidden');
}

function show_chart() {
    $(".land_view").removeAttr('hidden');
    $(".port_view").attr('hidden', '');
}

var ee;
$(window).on("orientationchange", function(event) {
    ee = event;
    $(window).one('resize', resize_checker);

});

function resize_checker() {
    if (is_mobile === false) {
        show_chart();
        return;
    }

    if (window.matchMedia("(orientation: portrait)").matches) {
        // console.log("P");
        hide_chart();
    }
    if (window.matchMedia("(orientation: landscape)").matches) {
        // console.log("L");
        show_chart();

        if (chart_loaded === false) {
            load_chart();
        }
    }
}

function load_chart() {
    get_standings();
                chart_loaded = true;
}

var chart_loaded = false;
var is_mobile = false;

$(document).ready(function() {
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        is_mobile = true;
        resize_checker()
    }
    else {
        show_chart();
        get_standings()
    }

    console.log(is_mobile);

});