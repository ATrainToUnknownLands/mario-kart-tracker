function formIsValid(form){
    // Check that the two entered positions aren't the same
    let positions = $(form).children(".position-select").map(function() { return $(this).val() }).get()
    let uniquePositions = [...new Set(positions)]

    if(positions.length != uniquePositions.length){
        console.log("Two positions the same!")
        return false
    }

    // Check that the track is one of the available selections
    let selectedStartTrack = $("#start-race-track").val()
    let selectedEndTrack = $("#end-race-track").val()

    let startExists = 0 != $(`#tracks option[value='${selectedStartTrack}']`).length;
    if(!startExists){ 
        console.log("Track doesn't exist!") 
        return false 
    }
    
    let endExists = 0 != $(`#tracks option[value='${selectedEndTrack}']`).length;
    if(!startExists){
        console.log("Track doesn't exist!") 
        return false 
    }
}

function submitData(form, path){
    form.attr("action", path);
    formIsValid(form)
    form.submit();
}

$(document).ready(function(){
    const nextButton = $("#submit-race");
    const prevButton = $("#previous-race");
    const raceForm = $("#race-entry");

    nextButton.on("click", function(){ submitData(raceForm, NEXT_RACE_URL) })
    prevButton.on("click", function(){ submitData(raceForm, PREV_RACE_URL) })
})
