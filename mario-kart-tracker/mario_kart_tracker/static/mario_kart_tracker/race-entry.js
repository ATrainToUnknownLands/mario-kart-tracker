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

    let startExists = 0 != $(`#tracks option[value="${selectedStartTrack}"]`).length;
    if(!startExists){ 
        console.log("Start track doesn't exist!") 
        return false 
    }
    
    let endExists = 0 != $(`#tracks option[value="${selectedEndTrack}"]`).length;
    if(!endExists){
        console.log("End track doesn't exist!") 
        return false 
    }

    return true
}

function submitData(form, path){
    form.attr("action", path);
    if(formIsValid(form)){
        form.submit();
    } else {
        alert("Form invalid. Please correct.")
    }
}

$(document).ready(function(){
    const nextButton = $("#submit-race");
    const prevButton = $("#previous-race");
    const raceForm = $("#race-entry");

    nextButton.on("click", function(){ submitData(raceForm, NEXT_RACE_URL) })
    prevButton.on("click", function(){ submitData(raceForm, PREV_RACE_URL) })
})
