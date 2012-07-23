$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});





$( document ).ready( function() {


$("#id_userid").change(function (){
    elegido=$(this).val();

    $.ajax({
        type     : 'POST',
        url      : "/caja/usuarios/consultar/",
        data     : { elegido: elegido},
        success  : function(data){
                   $("#id_username").val(data.username);
                   $("#id_first_name").val(data.first_name);
                   $("#id_last_name").val(data.last_name);
                   $("#id_email").val(data.email);
                   $("#id_phone_number").val(data.phone_number);
                   $("#id_cellphone").val(data.cellphone);
                   $("#id_address").val(data.address);
                   $("#id_username").attr("readonly", "true")
                   $("#id_first_name").attr("readonly", "true")
                   $("#id_last_name").attr("readonly", "true")
                   $("#id_username").addClass("readonly found")
                   $("#id_first_name").addClass("readonly")
                   $("#id_last_name").addClass("readonly")
        },
        error    : function(data){
                   $("#id_username").val("USUARIO NO EXISTENTE");
                   $("#id_first_name").val('');
                   $("#id_last_name").val('');
                   $("#id_email").val('');
                   $("#id_phone_number").val('');
                   $("#id_cellphone").val('');
                   $("#id_address").val('');
                   $("#id_username").removeAttr("readonly"); 
                   $("#id_first_name").removeAttr("readonly");
                   $("#id_last_name").removeAttr("readonly"); 
                   $("#id_username").removeClass("readonly found"); 
                   $("#id_first_name").removeClass("readonly");
                   $("#id_last_name").removeClass("readonly"); 


   } });
});			

});


$(document).ready(function(){
	// Parametros para e combo1
   $("#id_marca").change(function (){
   		$("#id_marca option:selected").each(function () {
			//alert($(this).val());
				elegido=$(this).val();
            if ($('#id_userid').val()>0) {    
				$.post("/caja/combo_dependiente/", { elegido: elegido }, function(data){
				$("#id_modelo").html(data);
			});
            }
            else{
				$.post("/autos/combo_dependiente/", { elegido: elegido }, function(data){
				$("#id_modelo").html(data);
			});

            }
			
        });
   })

});

$(document).ready(function(){
	// Parametros para e combo1
   $("#id_estado").change(function (){
   		$("#id_estado option:selected").each(function () {
			//alert($(this).val());
				elegido=$(this).val();
				$.post("/lugares/combo_dependiente/", { elegido: elegido }, function(data){
				$("#id_municipio").html(data);
			});			
        });
   })

});



$( document ).ready( function() {


$("#id_descripcion").charCount({
    allowed: 140,
    warning: 20,
    counterText: 'Caracteres gratis restantes: '
});


$("#id_paquete").change(function (){
	$("#id_paquete option:selected").each(function () {

    elegido=$(this).val();

    $.ajax({
        type     : 'POST',
        url      : "/caja/consultar_paquete/",
        data     : { elegido: elegido},
        success  : function(data){
                   $("#id_mintexto").val(data.min_texto);        
        },
        error    : function(data){
                   $("#id_mintexto").val(140);
   } });
});	
});	

});

