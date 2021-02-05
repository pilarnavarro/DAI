function get_runtime() {
    return new Promise((resolve, reject) => {
        let duraciones = {}
        $.getJSON('/api/episodios').done(function(respuesta) {
            $.each(respuesta, function(key, value) {
                if (!(value['season'] in duraciones)) {
                    duraciones[value['season']] = []
                }
                duraciones[value['season']].push([value['number'], value['runtime']])
            });
            resolve(duraciones)
        });
    })
}

async function draw_barchart(iden, min, max) {
    let width = $(iden).width();
    let duraciones = await get_runtime();
    let serie = []
    for (var key in duraciones) {
        if (key >= min && key <= max) {
            let dict = {
                name: "Temporada " + key,
                data: duraciones[key],
            }
            serie.push(dict)
        }
    }

    Highcharts.chart(iden, {
        chart: {
            type: 'column',
            width: width
        },
        title: {
            text: 'Duración episodios'
        },
        subtitle: {
            text: 'Temporadas ' + min + '-' + max
        },
        xAxis: {
            title: {
                text: 'Número de episodio'
            },
            accessibility: {
                rangeDescription: 'Range: 1 to 25'
            },
            tickInterval: 1
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Duración (min)'
            }
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: 'Episodio {point.x}: Duración {point.y} min'
        },
        plotOptions: {

            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                //pointWidth: 5
            }
        },
        series: serie
    });
}

$(async function() {
    await draw_barchart('bar_chart', 1, 10)
    await draw_barchart('bar_chart1', 1, 3)
    await draw_barchart('bar_chart2', 3, 5)
    await draw_barchart('bar_chart3', 5, 7)
    await draw_barchart('bar_chart4', 8, 10)
});