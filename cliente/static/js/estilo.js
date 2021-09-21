/*delete*/
	jQuery(document).ready(function($){
		  $(".js-delete-cliente").click(function () {
		    var btn = $(this);
		    $.ajax({
		      url: '/cliente/deletar/'+btn.attr("id")+'/',
		      type: 'get',
		      dataType: 'json',
		      beforeSend: function () {
		      	jQuery.noConflict(); 
		        $("#delete-cliente-modal").modal("show");
		      },
		      success: function (data) {
		        $("#delete-cliente-modal .modal-content").html(data.html_form);
		      }
		    });
		  });

		});

/*esconde e mostra o input de parcelas quando selecionado a opção correta*/
	window.onload = function(){
	    document.getElementById('pesquisa').onchange = function() {
	        if(this.value == 'agendamento'){
	            document.getElementById('data_ini').style.display = "block";
	        	document.getElementById('data_fin').style.display = "block";
	        	document.getElementById('input-sexo-oculto').style.display = "none";
	        } else if(this.value == 'qtd_processo'){ 
	            document.getElementById('data_ini').style.display = "none";
	        	document.getElementById('data_fin').style.display = "none";
	        	document.getElementById('input-sexo-oculto').style.display = "none";
	        }else if(this.value == 'sexo'){ 
	            document.getElementById('data_ini').style.display = "none";
	        	document.getElementById('data_fin').style.display = "none";
	        	document.getElementById('input-sexo-oculto').style.display = "block";
	        }
	    };
	
	};
	