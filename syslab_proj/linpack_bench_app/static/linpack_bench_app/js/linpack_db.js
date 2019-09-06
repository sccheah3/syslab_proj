/*$(document).ready(function () {
	var systable = $('#sysinfoTable').DataTable({
		"order": [[12, "desc"]]
	});
	$('.dataTables_length').addClass('bs-select');
	console.log(systable.search())
	console.log("hi")
});
*/

$(document).ready(function() {
    // Setup - add a text input to each footer cell
    //$('tfoot th').each( function () {
    $('.searchFilter').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" style="text-align:center; width:100px" placeholder="' + title +'" />' );
    } );
 
    // DataTable
    var table = $('#sysinfoTable').DataTable({
		"order": [[12, "desc"]]
	});
	$('.dataTables_length').addClass('bs-select');
 
    // Apply the search
    table.columns().every( function () {
        var that = this;
 
        $( 'input', this.footer() ).on( 'keyup change clear', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );
} );