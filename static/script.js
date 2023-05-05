$(function() {    
    // Global variables.
    var types = [];
    var header_count = 0;

    var get_data_types = function() {
        $.get('api/data/types', function(data) {
            types = JSON.parse(data);
            set_select_values($('#type_0'));
        });
    };

     var set_select_values = function(select_element) {
        for ( var i = 0; i < types.length; i++ ) { 
            $(select_element).append('<option value="' + types[i]['method'] + '">' + types[i]['label'] + '</option>')
        }
     };
    

    var add_header = function() {
        header_count++;

        var new_div = $('<div class="input-group mb-3" id="new_div_' + header_count + '"></div>');        
        var input_elem = $('<input type="text" id="name_' + header_count + '" class="form-control" placeholder="Header Name">');
        var select_elem = $('<select class="form-select" id="type_' + header_count + '""></select>');
        var delete_btn_elem = $('<button class="btn btn-danger" type="button" id="delete_' + header_count + '"><i class="bi bi-trash3"></i></button>');

        new_div.append(input_elem);
        new_div.append(select_elem);
        new_div.append(delete_btn_elem);

        $('#headers').append(new_div);

        set_select_values($('#type_' + header_count));
    };

    var build_header_data = function() {
        var headers = [];
        var header_elems = $('#headers').children();
        
        $('#status_msg').attr('class', 'alert alert-warning');
        $('#status_msg').text('Generating CSV...');
        
        for ( var i = 0; i < header_elems.length; i++ ) {
            var header_children = $(header_elems[i]).children();
            var header_name = '';
            var type_name = '';

            for ( var j = 0; j < header_children.length; j++ ) {
                if ( $(header_children[j]).attr('id').includes('name') ) {
                    header_name = $(header_children[j]).val();
                }

                if ( $(header_children[j]).attr('id').includes('type') ) {
                    type_name = $(header_children[j]).val();
                }

            }

            if ( header_name != '' && type_name != '' ) {
                headers.push({
                    'label': header_name,
                    'method': type_name
                });
            }   
        }

        console.log(headers);

        return headers;
    };

    var generate_csv = function(headers) {
        console.log(JSON.stringify(headers));

        var csv_file_name = uuid.v4();
        console.log(csv_file_name);

        $('#csv_file_name').val(csv_file_name);


        var rows = $('#rows').val();
        if ( rows == '' ) rows = 1;

        jQuery.ajax ({
            url: '/api/generate/csv/' + csv_file_name + '/' + rows,
            type: 'POST',
            data: JSON.stringify(headers),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
        }).done(function(response) {
            var formatted_str = '';
            
            for ( var i = 0; i < response.length; i++ ) {
                for ( var j = 0; j < response[i].length; j++ ) {
                    formatted_str += response[i][j] + ','
                }
                formatted_str += '\r\n';
            }

            $('#json_resp').text(formatted_str);

            $('#status_msg').attr('class', 'alert alert-success');
            $('#status_msg').html('Success! Your file is ready to be downloaded <a href="/download/' + csv_file_name + '">here</a>. Files will expire after 24 hours.');
        });
    };

    $('#add').click(function() {
        add_header();
    });

    $('#generate').click(function() {
        var header_data = build_header_data();
        generate_csv(header_data);
    });

    $('body').on('click', "[id^=delete]", function() {
        var num = this.id.slice(7);
        console.log('clicked delete_' + num);
        var parent = $(this).parent();
        console.log(parent);
        $(parent).remove();
    });

    get_data_types();

    console.log("Wee wee wee wee wee");


});