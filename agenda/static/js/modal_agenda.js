/*delete*/
jQuery(document).ready(function($){
	  $(".delete_agenda-js").click(function () {
	  	var btn = $(this);
	    $.ajax({
	      url: '/agenda/delete/'+btn.attr("id")+'/',
	      type: 'GET',
	      dataType: 'json',
	      beforeSend: function () {
	      	jQuery.noConflict(); 
	        $("#delete-agenda-modal").modal("show");
	      },
	      success: function (data) {
	        $("#delete-agenda-modal .modal-content").html(data.html_form);
	      }
	    });
	  });

	});