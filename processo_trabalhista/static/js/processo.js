/*funcao que chama o modal */
jQuery(document).ready(function($){
  $(".js-create-processo").click(function () {
    $.ajax({
      url: '/processo/add/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#add_processo-modal").modal("show");
      },
      success: function (data) {
        $("#add_processo-modal .modal-content").html(data.html_form);
      }
    });
  });
});

/*delete*/
jQuery(document).ready(function($){
	  $(".js-delete-processo").click(function () {
	   var btn = $(this);
	    $.ajax({
	      url: '/processo/deletar/'+btn.attr("id")+'/',
	      type: 'get',
	      dataType: 'json',
	      beforeSend: function () {
	      	jQuery.noConflict(); 
	        $("#processo-modal").modal("show");
	      },
	      success: function (data) {
	        $("#processo-modal .modal-content").html(data.html_form);
	      }
	    });
	  });

	});