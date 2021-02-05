function Eliminar(ident) {
    let urlApi = '/api/episodios/' + ident
    $(function() {
        console.log(urlApi)
        $.ajax({
            url: urlApi,
            type: 'DELETE',
        });
        $("tbody").empty();
        $.getJSON('/api/episodios').done(mostrar);
    });
}

function mostrar(respuesta) {
    $.each(respuesta, function(key, value) {
        $("tbody").append(`<tr>
<td>${value['name']}</td>
<td>${value['id2']}</td>
<td><a href='${value['url']}'>${value['url']}</a></td>
<td>${value['season']}</td>
<td>${value['number']}</td>
<td>${value['airdate']}</td>
<td>${value['airtime']}</td>
<td>${value['airstamp']}</td>
<td>${value['runtime']}</td>
<td>${value['summary']}</td>
<td> 
<center>
<a class="btn btn-danger btn-sm" onclick="Eliminar('${value.id}')">Borrar</a>
</center>
</td>
</tr>`)
    });
}

$(document).ready(function() {
    $.getJSON('/api/episodios').done(mostrar);
    $("#buscar_season").change(function() {
        let value = $(this).val();
        console.log(value);
        $("tbody").empty();
        $.getJSON('/api/episodios', {
            season: value
        }).done(mostrar);
    });
    $("#buscar_number").change(function() {
        let value = $(this).val();
        console.log(value);
        $("tbody").empty();
        $.getJSON('/api/episodios', {
            number: value
        }).done(mostrar);
    });
    $("#buscar_estreno").change(function() {
        let value = $(this).val();
        console.log(value);
        $("tbody").empty();
        $.getJSON('/api/episodios', {
            airdate: value
        }).done(mostrar);
    });
    $("#buscar_nombre").change(function() {
        let value = $(this).val();
        console.log(value);
        $("tbody").empty();
        $.getJSON('/api/episodios', {
            name: value
        }).done(mostrar);
    });
    $("#buscar_resumen").change(function() {
        let value = $(this).val();
        console.log(value);
        $("tbody").empty();
        $.getJSON('/api/episodios', {
            summary: value
        }).done(mostrar);
    });
});