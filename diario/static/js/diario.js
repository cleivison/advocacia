/*delete*/
	jQuery(document).ready(function($){
		  $(".js-delete-file").click(function () {
		   var btn = $(this);
	    	$.ajax({
	      	  url: '/diario/deletar/'+btn.attr("id")+'/',
		      type: 'get',
		      dataType: 'json',
		      beforeSend: function () {
		      	jQuery.noConflict(); 
		        $("#delete-documento-modal").modal("show");
		      },
		      success: function (data) {
		        $("#delete-documento-modal .modal-content").html(data.html_form);
		      }
		    });
		  });

		});