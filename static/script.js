$(function() {    
    // Global variables. 
    /*var random_index = Math.floor(Math.random() * 5757);
    var num_guesses = 0;
    var guess_history = [];
    var attempts_left = 5;
    var is_correct = false;
    var invalid_letters = '';
    var sec = 0;
    var timer_started = false;
    var timer = null;

    if ( window.location.pathname.length > 1 ) {
        random_index = parseInt(window.location.pathname.split('/')[1]);
        if ( random_index == 0 ) {
            $('#prev_word').prop('disabled', true);
        }
    }

    var remove_duplicate_in_string = function(str) {
        return str.split('').filter(function(item, pos, self) {
            return self.indexOf(item) == pos;
        }).join('');
    };

    var format_str = function(str) {
        var spaced_letters = '';
        for ( var i = 0; i < str.length; i++ ) {
            spaced_letters = spaced_letters + str[i] + ' ';
        }
        return spaced_letters;
    };

    var sort_str = function(str) {
        return str.split('').sort().join('');
    };

    var is_alpha_only = function(str) {
        var len = 0;
        
        for ( var i = 0, len = str.length; i < len; i++ ) {
            var code = str.charCodeAt(i);
            if ( !(code > 64 && code < 91) &&  !(code > 96 && code < 123) ) {
                return false;
            }
        }

        return true;
    };

    var pad = function(val) {
        return val > 9 ? val : "0" + val;
    };

    var submit_guess = function() {
        if ( !timer_started ) {
            timer_started = true;
            timer = setInterval(function() {
                $("#seconds").html(pad(++sec % 60));
                $("#minutes").html(pad(parseInt(sec / 60, 10)));
            }, 1000);
        }

        var guess = $('#guess').val().toUpperCase();
        
        if ( is_alpha_only(guess) ) {
            if ( attempts_left > 0 ) {
                $.get('api/word/guess/' + guess + '/' + random_index, function(data) {
                    var response_obj = JSON.parse(data);
                    
                    if ( response_obj.hasOwnProperty('error') ) {
                        $('#guess').fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100);
                    }

                    else {
                        num_guesses++;
                        
                        if ( !$('#unlimited_guesses').is(':checked') ) {
                            attempts_left--;
                        }

                        var table_row = '';
                    
                        var resp_row = '<tr>';
                        var guess_row = '<tr>';
                        
                        var split_guess = guess.split('');
                        var split_resp = response_obj['alignment_code'].split('');
                        
                        var current_guess = [];

                        for ( var i = 0; i < split_guess.length; i++ ) {
                            var resp_class = 'table-danger';
                            
                            switch ( split_resp[i] ) {
                                case split_guess[i]:
                                    resp_class = 'table-success';
                                    break;
                                case '*':
                                    resp_class = 'table-warning';
                                    break;
                                case '_':
                                    resp_class = 'table-danger';
                                    break;
                            }

                            guess_row += '<td class="' + resp_class + ' text-center">' + split_guess[i] + '</td>';    
                            current_guess.push(resp_class);

                        }

                        guess_history.push(current_guess);
                        guess_row += '</tr>';
                        table_row += guess_row;

                        $('#answer_word').append(table_row);
                        $('#remaining_letters').text(format_str(response_obj['remaining_letters']));
                        
                        invalid_letters += response_obj['invalid_letters'];
                        invalid_letters = remove_duplicate_in_string(invalid_letters);
                        invalid_letters = sort_str(invalid_letters);

                        if ( guess.toUpperCase() == response_obj['alignment_code'] ) {
                            $('#reveal_word').html("Nice work! The word is: <a href='https://www.merriam-webster.com/dictionary/" + guess + "'>" + guess.toUpperCase() + "</a>");
                            $('#time_elapsed').text("Time elapsed: " + pad(parseInt(sec / 60, 10)) + ":" + pad(++sec % 60));
                            $('#guess_count').text("Number of guesses: " + num_guesses);
                            $('#results-modal').modal('show');
                            $('#take_guess').prop('disabled', true);
                            is_correct = true;
                            clearInterval(timer);

                        }

                        else {
                            if ( attempts_left == 0 ) {
                                $.get('api/word/' + random_index, function(data) {
                                    $('#take_guess').prop('disabled', true);
                                    $('#reveal_word').html("Sorry! You are out of guesses. The word is: <a href='https://www.merriam-webster.com/dictionary/" + data + "'>" + data.toUpperCase() + "</a>");
                                    $('#results-modal').modal('show');
                                    is_correct = true;
                                    clearInterval(timer);
                                }); 
                            }
                        }
                    }
                });
            }
        } 
    };

    var get_char_from_el = function(el) {
        var char = '';

        switch ( el ) {
            case 'table-success':
                char = '🟩';
                break;
            case 'table-warning':
                char = '🟨';
                break;
            case 'table-danger':
                char = '🟥';
                break;
        }

        return char;
    }

    var convert_results = function() {
        var text_results = '';

        for ( var i = 0; i < guess_history.length; i++ ) {
            for ( var j = 0; j < guess_history[i].length; j++ ) {
                text_results += get_char_from_el(guess_history[i][j]);
            }

            text_results += '\n';
        }

        return text_results;
    };

    // $('#header').text('#' + random_index);

    $('#new_word').click(function() {
        window.location.replace("/");
    });

    $('#prev_word').click(function() {
        window.location.replace("/" + (random_index - 1));
    });

    $('#next_word').click(function() {
        window.location.replace("/" + (random_index + 1));
    });

    $("#guess").keypress( function(e) {
        var chr = String.fromCharCode(e.which);
        if ( invalid_letters.indexOf(chr.toUpperCase()) > -1 ) {
            if ( !$('#wrong_letters').is(':checked') )  {
                return false;
            }
        }
    });

    $('#take_guess').click(function() {
        if ( $('#guess').val().length == 5 ) {
            if ( !is_correct ) {
                submit_guess();
                $('#guess').val('');
            }
        }
    });

    $('#guess').keydown(function (e) {
        if ( e.keyCode == 13 ) {
            if ( $('#guess').val().length == 5 ) {
                if ( !is_correct ) {
                    submit_guess();
                    $('#guess').val('');

                }
            }
        }
    });

    $('#share').click(function() {
        var results = convert_results();
        var output_results = 'wordguess.online/' + random_index + '\n' + results 
        + 'Number of guesses: ' + num_guesses 
        + '\nSolved in: ' + pad(parseInt(sec / 60, 10)) + ":" + pad(++sec % 60)
        + '\nUnlimited guesses: ' + ($('#unlimited_guesses').is(':checked') ? ' on ' : ' off ')
        + '\nIncorrect letters allowed: ' + ($('#wrong_letters').is(':checked') ? ' on ' : ' off ');
        navigator.clipboard.writeText(output_results);
    });

    $('#close_button').click(function() {
        $('#results-modal').modal('hide');

    });

    $('#close_button_about').click(function() {
        $('#about-modal').modal('hide');

    });

    $('#about_modal_btn').click(function() {
        $('#about-modal').modal('show');
    });
*/

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
        var select_elem = $('<select class="form-control" id="type_' + header_count + '""></select>');

        new_div.append(input_elem);
        new_div.append(select_elem);

        $('#headers').append(new_div);

        set_select_values($('#type_' + header_count));
    };

    var delete_header = function(select_element) {

    };

    var build_header_data = function() {
        var headers = [];
        var header_elems = $('#headers').children();
        
        for ( var i = 0; i < header_elems.length; i++ ) {
            var header_children = $(header_elems[i]).children();
            var header_name = $(header_children[0]).val();
            var type_name = $(header_children[1]).val();
            
            headers.push({
                'label': header_name,
                'method': type_name
            });
        }

        console.log(JSON.stringify(headers));

        jQuery.ajax ({
            url: '/api/generate/csv/winnie.csv/25',
            type: 'POST',
            data: JSON.stringify(headers),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function(data) {
                console.log(data)
            }
        });

        /*$.post('/api/generate/csv/winnie.csv/25', "HELLO", function(data) {
            console.log(data);
        });*/
    };

    $('#add').click(function() {
        add_header();
    });

    $('#generate').click(function() {
        var header_data = build_header_data();
    });

    get_data_types();

     console.log("Wee wee wee wee wee");


});