$(function() {
    $('#id_ubigeo_0 option:contains("Lima")').prop('selected', true);
    //$('#id_ubigeo_0 option:contains("---------")').text('Seleccionar');
    //console.log($('#id_ubigeo_0').val());
    //if($('#id_ubigeo_0').val() != undefined){
        //console.log('getProvincias')
        getProvincias($('#id_ubigeo_0').val(), null, null, true);
        
        //$('#id_ubigeo_2 option:contains("Lima")').prop('selected', true);
    //}
    //console.log($('#id_ubigeo_0').val())
    //getProvincias($('#id_ubigeo_0').val());
});

function getProvincias(id,value_provincia,value_distrito, ini){
    var provincia = $("#id_ubigeo_1");
    provincia.find('option').remove();
    provincia.append("<option value='' selected>---------</option>");
    //provincia.append("<option value='' selected>Seleccionar</option>");
    $.getJSON('/ubigeo/provincia/json/?r='+id, function(data){
        $.each(data, function(key,value){
            if(key == 0){
                if(value_provincia != null)
                    getDistritos(value_provincia,value_distrito);
                else
                    getDistritos(value.pk,value_distrito);
            }
            if(value_provincia == value.pk)
                provincia.append("<option value='"+value.pk+"' selected>"+value.fields.name+"</option>");
            else
                provincia.append("<option value='"+value.pk+"'>"+value.fields.name+"</option>");
            if(ini){
                $('#id_ubigeo_1 option:contains("Lima")').prop('selected', true);
                getDistritos($('#id_ubigeo_1').val(), null, true)
            }
        });
    });
}

function getDistritos(id,value_distrito, ini){
    var distrito = $("#id_ubigeo_2");
    distrito.find('option').remove();
    distrito.append("<option value='' selected>---------</option>");
    //distrito.append("<option value='' selected>Seleccionar</option>");
    $.getJSON('/ubigeo/distrito/json/?d='+id, function(data){
        $.each(data, function(key,value){
            if(value_distrito == value.pk)
                distrito.append("<option value='"+value.pk+"' selected>"+value.fields.name+"</option>");
            else
                distrito.append("<option value='"+value.pk+"'>"+value.fields.name+"</option>");
            if(ini){
                $('#id_ubigeo_2 option:contains("Lima")').prop('selected', true);
            }
        });
    });
}
