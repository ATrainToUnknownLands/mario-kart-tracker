let selectedGame = "";
let selectedGameHtml = "";

$(document).ready(function() {
    $("div.session_form").hide()
    
    // Show the appropriate game's settings form when selected
    $("input[name$='game_version']").click(function() {
        selectedGame = $(this).val();
        selectedGameHtml = selectedGame.replace("_", "-")

        // Clear any player fieldsets (in case switching between the two)
        $("fieldset[name$='player-settings']").remove()
        $(":submit").remove()
        $("div.session_form").hide();
        $(`#${selectedGame}_form`).show();
    });

    // Add the appropriate number of player settings boxes
    $("#mk-world-no-players").on('change', function() {
        add_player_fieldsets(this)
    })
    $("#mk8-no-players").on('change', function() {
        add_player_fieldsets(this)
    })
});

function get_player_defaults(event) {
    let selectedPlayer = event.target.value;
    let playerNo = event.data.player_no;

    // Make the request to the server
    $.get("../player_default", {player_id: selectedPlayer, game_version: selectedGame})
        .done(function(data){
            // For each returned value, fill in the field
            for(const [key, value] of Object.entries(data)){
                $(`#${selectedGameHtml}-player${playerNo}-${key}`).val(value);
            }
        })
        .fail(function(error){
            const statusCode = error.status;
            if(statusCode == 404){
                // If 404, no defaults found, so do nothing
                console.log("No defaults found")
            }
            else {
                // Otherwise, throw an error
                console.error(error)
            }
        })
}

function add_player_fieldsets(input_element) {
    // Limit to only 4 players
    let no_players = Math.min($(input_element).val(), 4);

    // Reset the input in case it's > 4
    $(input_element).val(no_players)

    // Clear any existing fieldsets
    $("fieldset[name$='player-settings']").remove()
    $(":submit").remove()

    // For each player, append all of the setup fields
    for(let p = 0; p < no_players; p++){
        player_no = p + 1
        let html = ''
        
        if(selectedGame == "mk8") {
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
        else if(selectedGame == "mk_world") {
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
        $(`#${selectedGameHtml}-session-setup`).append(html)
        
        // When the player is selected, get the defaults
        let player_select = $(`#${selectedGameHtml}-player${player_no}`)
        player_select.on("change", {player_no: player_no}, get_player_defaults)

        // Add the players to the select options
        $("#player-list option").each(function(){
            $(this).clone().appendTo($(`#${selectedGameHtml}-player${player_no}`))
        })
    }

    submit_button = `<input type="submit" value="Start">`
    $("form[name$='session-setup']").append(submit_button)
}