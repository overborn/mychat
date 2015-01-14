$(document).ready(function() {
    $.get($SCRIPT_ROOT + '/suggest_channel', {suggestion: ''}, function(data){
         $('#channs').html(data);
        });
	$('#suggestion').keyup(function(){
	    var query= $(this).val();	    
	    $.get($SCRIPT_ROOT + '/suggest_channel', {suggestion: query}, function(data){
	     $('#channs').html(data);
	    });
	});

});