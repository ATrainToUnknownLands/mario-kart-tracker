$(document).ready(function() {
    $("div.session_form").hide()
    
    // Show the appropriate game's settings form when selected
    $("input[name$='game_version']").click(function() {
        var selected_game = $(this).val();
        // Clear any player fieldsets (in case switching between the two)
        $("fieldset[name$='player-settings']").remove()
        $(":submit").remove()
        $("div.session_form").hide();
        $("#" + selected_game).show();
    });

    // Add the appropriate number of player settings boxes
    $("#mk-world-no-players").on('change', function() {
        add_player_fieldsets(this, "mk-world")
    })
    $("#mk8-no-players").on('change', function() {
        add_player_fieldsets(this, "mk8")
    })
});

function add_player_fieldsets(input_element, game_version) {
    // Limit to only 4 players
    var no_players = Math.min($(input_element).val(), 4)

    // Reset the input in case it's > 4
    $(input_element).val(no_players)

    // Clear any existing fieldsets
    $("fieldset[name$='player-settings']").remove()
    $(":submit").remove()

    for(let p = 0; p < no_players; p++){
        player_no = p + 1
        var html = ''
        
        if(game_version == "mk8") {
            html = `<fieldset name="player-settings">
                <legend>Player Settings: Player ${player_no}</legend>
                <label for="mk8-player${player_no}">Player</label>
                <select name="player-select${player_no}" id="mk8-player${player_no}"></select><br>
                <label for="mk8-player${player_no}-character">Character</label>
                <input type="text" name="player${player_no}-character" id="mk8-player${player_no}-character" list="mk8-characters"><br>
                <label for="mk8-player${player_no}-vehicle">Vehicle</label>
                <input type="text" name="player${player_no}-vehicle" id="mk8-player${player_no}-vehicle" list="mk8-vehicles">

                <label for="mk8-player${player_no}-wheel">Wheel</label>
                <input type="text" name="player${player_no}-wheel" id="mk8-player${player_no}-wheel" list="mk8-wheels">

                <label for="mk8-player${player_no}-glider">Glider</label>
                <input type="text" name="player${player_no}-glider" id="mk8-player${player_no}-glider" list="mk8-gliders">
            </fieldset>`
        }
        else if(game_version == "mk-world") {
            html = `<fieldset name="player-settings">
                <legend>Player Settings: Player ${player_no}</legend>
                <label for="mk-world-player${player_no}">Player</label>
                <select name="player-select${player_no}" id="mk-world-player${player_no}"></select><br>
                <label for="mk-world-player${player_no}-character">Character</label>
                <input type="text" name="player${player_no}-character" id="mk-world-player${player_no}-character" list="mk-world-characters"><br>
                <label for="mk-world-player${player_no}-vehicle">Vehicle</label>
                <input type="text" name="player${player_no}-vehicle" id="mk-world-player${player_no}-vehicle" list="mk-world-vehicles">
            </fieldset>`
        }
        $(`#${game_version}-session-setup`).append(html)

        var player_select = $(`#${game_version}-player${player_no}`)
        console.log(player_select)

        // Add the players to the select options
        $("#player-list option").each(function(){
            $(this).clone().appendTo($(`#${game_version}-player${player_no}`))
        })
    }

    submit_button = `<input type="submit" value="Start">`
    $("form[name$='session-setup']").append(submit_button)
}