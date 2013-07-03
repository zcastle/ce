$(function() {
    /**/
    $.datepicker.regional['es'] = {
        closeText: 'Cerrar',
        prevText: '&#x3c;Ant',
        nextText: 'Sig&#x3e;',
        currentText: 'Hoy',
        monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
        dayNames: ['Domingo','Lunes','Martes','Mi&eacute;rcoles','Jueves','Viernes','S&aacute;bado'],
        dayNamesShort: ['Dom','Lun','Mar','Mi&eacute;','Juv','Vie','S&aacute;b'],
        dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''};
    $.datepicker.setDefaults($.datepicker.regional['es']);
    /**/
	$('#id_fe_nacimiento').datepicker({
		changeMonth: true,
		changeYear: true,
		dateFormat: 'dd/mm/yy',
		/*minDate: new Date('1990/10/25'),*/
        yearRange: '1900:c'/*,
		maxDate: new Date(),
        onClose: function(dateText, inst) { 
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1));
        }*/
    });

    $('#id_fe_periodo_ini, #id_fe_periodo_fin').datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'mm/yy',
        /*minDate: new Date('1990/10/25'),*/
        yearRange: '1900:c',
        showButtonPanel: true,
        onClose: function(dateText, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1));
        }
    });

    $("#id_fe_periodo_ini, #id_fe_periodo_fin").focus(function () {
        $(".ui-datepicker-calendar").hide();
        $("#ui-datepicker-div").position({
            my: "center top",
            at: "center bottom",
            of: $(this)
        });
    });

    $('#lnk-postulante').click(function(){
    	var div = $('<div></div>');
    	div.load('/postulante/ingresar').dialog({
    		title: 'Ingresar a Coopsol Empleos',
    		width: 545,
    		modal: true,
    		resizable: false,
    		show: 'explode',
      		hide: 'explode'
    	});
    });

    var f = new Date();
    var meses = new Array ('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre');
    var diasSemana = new Array('Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado');
    $('.fecha').html(diasSemana[f.getDay()] + ', ' + f.getDate() + ' de ' + meses[f.getMonth()] + ' del ' + f.getFullYear());

    $('#id_ubigeo_1').before('<label for="id_ubigeo_1">Provincia:</label>');
    $('#id_ubigeo_2').before('<label for="id_ubigeo_2">Distrito:</label>');

    //$('#id_fe_periodo_fin').after('<p><label for="id_fl_actualidad">Actualidad:</label> <input type="checkbox" name="fl_actualidad" id="id_fl_actualidad"></p>')
    //$('#id_fe_periodo_fin').after('<label for="id_fl_actualidad">Actualidad:</label> <input type="checkbox" name="fl_actualidad" id="id_fl_actualidad">')

    $('#id_fl_actualidad').click(function(t){
        if(this.checked){
            $('#id_fe_periodo_fin').attr('disabled', true)
        } else {
            $('#id_fe_periodo_fin').attr('disabled', false)
        }
    })

    $(".solo-numeros").numeric({
        decimal: false, 
        negative: false
    }, function() {
        alert("Positive integers only");
        this.value = "";
        this.focus();
    });

    $('#btnRegistrar').click(function(){
        var chk = $('input#chkTyc')[0].checked;
        if(chk){
            return true;
        }else{
            $('.errorlist2').css('display', 'inline')
            return false;
        }
    })

    //$('input[type="file"]').customFileInput();

    $('.cortar-remitente').each(function(){
        var longitud = 22;
        if($(this).text().length > longitud){
            var texto = $(this).text().substring(0, longitud);
            $(this).html(texto+'<span> ...</span>');
     
        };
    });

    $('.cortar-asunto').each(function(){
        var longitud = 60;
        if($(this).text().length > longitud){
            var texto = $(this).text().substring(0, longitud);
            $(this).html(texto);
            $(this).html(texto+' ...');
        };
    });

    if($('input#id_fl_licencia').checked){
        $('select#id_tipolicencia').attr('disabled', false)
        $('input#id_fl_auto_propio').attr('disabled', false)
    } else {
        $('select#id_tipolicencia').attr('disabled', true)
        $('input#id_fl_auto_propio').attr('disabled', true)
    }

    $('input#id_fl_licencia').click(function(t){
        if(this.checked){
            $('select#id_tipolicencia').attr('disabled', false)
            $('input#id_fl_auto_propio').attr('disabled', false)
        } else {
            $('select#id_tipolicencia').attr('disabled', true)
            $('input#id_fl_auto_propio').attr('disabled', true)
        }
    })

    $('a.ico-eliminar').click(function(){
        var btn = $(this);
        var div = $('<div>Desea proceder con la eliminacion?</div>');
        div.dialog({
            title: 'Mensaje de confirmacion',
            resizable: false,
            modal: true,
            buttons: {
                'Aceptar': function() {
                    window.location.href = btn.attr('href');
                    $(this).dialog('close');
                },
                Cancel: function() {
                    $(this).dialog('close');
                }
            }
        });
        return false;
    });

    var _minLength = 3;

    $('#id_institucion').autocomplete({
        source: function(request, response){
            $.ajax({
                url: "/universidad-json/"+request.term,
                dataType: "json",
                success: function(data){
                    response($.map(data.data, function(item){
                        return {
                            label: item.name,
                            value: item.name
                        }
                    }));
                }
            });
        },
        minLength: _minLength
    });

    $('#id_carrera').autocomplete({
        source: function(request, response){
            $.ajax({
                url: "/carrera-json/"+request.term,
                dataType: "json",
                success: function(data){
                    response($.map(data.data, function(item){
                        return {
                            label: item.name,
                            value: item.name
                        }
                    }));
                }
            });
        },
        minLength: _minLength
    });

    $('#id_idioma').autocomplete({
        source: function(request, response){
            $.ajax({
                url: "/idioma-json/"+request.term,
                dataType: "json",
                success: function(data){
                    response($.map(data.data, function(item){
                        return {
                            label: item.name,
                            value: item.name
                        }
                    }));
                }
            });
        },
        minLength: _minLength
    });

    $('#id_programa').autocomplete({
        source: function(request, response){
            $.ajax({
                url: "/programa-json/"+request.term,
                dataType: "json",
                success: function(data){
                    response($.map(data.data, function(item){
                        return {
                            label: item.name,
                            value: item.name
                        }
                    }));
                }
            });
        },
        minLength: _minLength
    });

    $('.col-avanzado').hide();

    $('#busquedaAvanzda').click(function(event){
        //console.log('Click');
        //event.preventDefault();
        if ($('.col-avanzado-2').is(':visible')) {
            $('.col-avanzado-2').hide('slow')
        } else {
            mostrarDistritos();
            mostrarAreas(null);
            $('.col-avanzado-2').show('slow')
        }
    })

    function mostrarDistritos(){
        var distritos = $("#id_distritos");
        distritos.find('option').remove();
        var url = "/distritos-json/";
        var option = "<option value selected>---------</option>";
        distritos.append(option);
        $.getJSON(url, function(data){
            $.each(data, function(key, value){
                var option = "<option value='" + value.id + "'>" + value.nombre + "</option>";
                distritos.append(option);
            });
        });
    }

    function mostrarAreas(distrito_id){
        var areas = $("#id_areas");
        areas.find('option').remove();
        var url;
        if (distrito_id)
            var url = "/areas-json/?distrito_id="+distrito_id;
        else
            var url = "/areas-json/";

        var option = "<option value selected>---------</option>";
        areas.append(option);
        $.getJSON(url, function(data){
            $.each(data, function(key, value){
                var option = "<option value='" + value.id + "'>" + value.nombre + "</option>";
                areas.append(option);
            });
        });
    }

    $('#id_distritos').change(function(){
        mostrarAreas(this.value);
        /*var v = $('#text_buscar');
        var texto = $(this).find('option:selected').text();
        texto = texto.substring(0, texto.length-3)
        console.log(texto);
        v.val(this.value);*/
        
    });

    $('#btnBusquedaAvanzada').click(function(){
        var distrito = $('#id_distritos').find('option:selected').text();
        var a = distrito.length-distrito.indexOf('(');
        distrito = distrito.substring(0, distrito.length-a);
        //console.log(distrito);

        var area = $('#id_areas').find('option:selected').text();
        var a = area.length-area.indexOf('(');
        area = area.substring(0, area.length-a);
        //console.log(area);

        var text_buscar = '';

        if(distrito!='---------' && distrito.length>0){
            text_buscar = distrito;
        }

        if(area!='---------' && area.length>0){
            if (text_buscar.length==0){
                text_buscar = area;
            } else {
                text_buscar = text_buscar+'+'+area;
            }
        }
        //console.log(text_buscar);
        window.location.href = '/buscar/?text_buscar='+text_buscar;
        return false;
    })

    $('#id_ubigeo_0').prev('label').text('Departamento:');


    var form_count = 0; //$("[name=extra_field_count]");

    $("#add-another").click(function() {
        element = $('<input type="text" />');
        element.attr('name', 'extra_field_' + form_count);
        element.attr('class', 'add-field');
        element.hide();
        //$("#form-crear").append(element);
        // build element and append it to our forms container
        $("#add-another").before(element);
        element.show('slow');

        form_count ++;
        $("[name=extra_field_count]").val(form_count);
        // increment form count so our view knows to populate 
        // that many fields for validation
        return false;
    })
    $('.grupo').mouseenter(function(event){
        event.preventDefault();
        $('.grupo ul').css('visibility', 'visible');
        $(this).animate({
            height: '290px'
        }, 300);
    });

    $('.grupo').mouseleave(function(event){
        event.preventDefault();
        $(this).animate({
            height: '20px'
        }, 300, function(){
            $('.grupo ul').css('visibility', 'hidden');
        });
    });
    
    //console.log('animate');
    //$('div#divfull').width(940);
/*
*/
});