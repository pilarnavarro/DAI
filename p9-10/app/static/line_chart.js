function get_dates() {
    return new Promise((resolve, reject) => {
        let fechas = {}
        $.getJSON('/api/episodios').done(function(respuesta) {
            $.each(respuesta, function(key, value) {
                if (!(value['season'] in fechas)) {
                    fechas[value['season']] = []
                }
                fechas[value['season']].push([value['number'], Date.parse(value['airdate'])])
            });
            resolve(fechas)
        });
    })
}

function get_dates_first_episode() {
    return new Promise((resolve, reject) => {
        let fechas = []
        $.getJSON('/api/episodios').done(function(respuesta) {
            $.each(respuesta, function(key, value) {
                if (value['number'] == 1) {
                    fechas.push([value['season'], Date.parse(value['airdate'])])
                }
            });
            resolve(fechas)
        });
    })
}

async function draw_linechart_first_episode() {
    let fechas = await get_dates_first_episode();
    Highcharts.chart('line_chart2', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Fechas de estreno'
        },
        subtitle: {
            text: 'Primer episodio de cada temporada'
        },
        xAxis: {
            title: {
                text: 'Temporada'
            },
            accessibility: {
                rangeDescription: 'Range: 1 to 10'
            },
            tickInterval: 1
        },
        yAxis: {
            title: {
                text: 'Fechas'
            },
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%e. %b',
                month: '%b \'%y',
                year: '%Y'
            },
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: 'Temporada {point.x}: {point.y:%e. %b %Y}'
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: false
                },
            },
            series: {
                marker: {
                    enabled: true,
                },
            }
        },
        legend: {
            enabled: false
        },
        series: [{
            name: "Primer episodio",
            data: fechas
        }],
    });
}

async function draw_linechart() {
    let fechas = await get_dates();
    let serie = []
    for (var key in fechas) {
        let dict = {
            name: "Temporada " + key,
            data: fechas[key],
        }
        serie.push(dict)
    }

    Highcharts.chart('line_chart', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Fechas de estreno'
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
            title: {
                text: 'Fechas'
            },
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%e. %b',
                month: '%b \'%y',
                year: '%Y'
            },
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: 'Episodio {point.x}:{point.y:%e. %b %Y}'
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: false
                },
            },
            series: {
                marker: {
                    enabled: true
                },
            }
        },
        // legend: {
        //     layout: 'vertical',
        //     align: 'right',
        //     verticalAlign: 'middle'
        // },
        series: serie,
    });
}

$(async function() {
    await draw_linechart()
    await draw_linechart_first_episode()
});