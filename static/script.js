// Fade header image on scroll and remove the "Scroll to Generate" banner when the user scrolls down
const checkpoint = 300;
var banner = document.getElementById("banner");
var header_image = document.getElementById("header-image");
var instrument;
var chosen_instrument;
var chosen_tonality;
var tonality;
var tempo;
var key;
var checked = 0;

function start_functions() {
  checked = 0;
}

window.addEventListener("scroll", () => {
  console.log("Scrolling");
  const currentScroll = window.pageYOffset;
  if (currentScroll <= checkpoint) {
    opacity = 1 - currentScroll / checkpoint;
  } else {
    opacity = 0;
    banner.classList.add("hide");
    header_image.classList.add("grow");
  }
  document.querySelector(".header-image .img").style.opacity = opacity;
});

function choose_instrument(instrument) {
  var selected = document.getElementById(instrument);
  selected.classList.toggle("selected");
  this.instrument = instrument
  chosen_instrument = instrument
}

function set_instrument(instrument) {
  this.instrument = instrument
}

function choose_tonality(tonality) {
  this.tonality = tonality
  chosen_tonality = tonality
}

function get_tempo() {
  this.tempo = document.getElementById("slider-text").innerHTML;
  return parseInt(tempo, 10);
}

function set_tempo(tempo) {
  this.tempo = tempo;
}

function get_key() {
  this.key = document.getElementById("keys").value;
  return key;
}

function check_if_all_chosen() {
  if (chosen_instrument == null || chosen_tonality == null || tempo == null) {
    alert("Please select all parameters.\n\nOtherwise on the next click of the \"Generate\" button, the program will default to: \n\nInstrument: Piano\nKey: C Major\nTempo: 120 bpm");
    this.checked = 1;
    return false;
  }
  return true;
}

function double_check_if_all_chosen() {
  if (chosen_instrument == null || chosen_tonality == null || tempo == null) {
    return false;
  }
  return true;
}

function send_parameters() {
  console.log("checked: ", this.checked)
  instrument = chosen_instrument;
  tonality = chosen_tonality;
  var instrument_temp = "piano";
  var tonality_temp = "major";
  var tempo_temp = 120;
  tempo = get_tempo();
  key = get_key();

  if (checked == 0) {
    if (check_if_all_chosen()) {
      var instrument_send = instrument; 
      var tonality_send = tonality; 
      var tempo_send = tempo; 
      var key_send = key; 

      console.log("instrument: ", instrument_send);
      console.log("tonality: ", tonality_send);
      console.log("tempo: ", tempo_send);
      console.log("key: ", key_send);
      
      alert("The song is being created!\nThis could take up to 15 minutes.");

      fetch('/run-script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({instrument: instrument_send, tonality: tonality_send, tempo: tempo_send, key: key_send}),
      })
      .then(response => response.text())
      .then(message => alert(message))
      .catch(error => console.error('Error:', error));
    }
  } else {
    if (double_check_if_all_chosen()) {
      var instrument_send = instrument; 
      var tonality_send = tonality; 
      var tempo_send = tempo; 
      var key_send = key; 

      console.log("instrument: ", instrument_send);
      console.log("tonality: ", tonality_send);
      console.log("tempo: ", tempo_send);
      console.log("key: ", key_send);

      alert("The song is being created!\nThis could take up to 15 minutes.");

      fetch('/run-script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({instrument: instrument_send, tonality: tonality_send, tempo: tempo_send, key: key_send}),
      })
      .then(response => response.text())
      .then(message => alert(message))
      .catch(error => console.error('Error:', error));
    }
    else {
      var instrument_send = instrument_temp; 
      var tonality_send = tonality_temp; 
      var tempo_send = tempo_temp; 
      var key_send = get_key();

      console.log("instrument: ", instrument_send);
      console.log("tonality: ", tonality_send);
      console.log("tempo: ", tempo_send);
      console.log("key: ", key_send);
      
      alert("The song is being created!\nThis could take up to 15 minutes.");
      
      fetch('/run-script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({instrument: instrument_send, tonality: tonality_send, tempo: tempo_send, key: key_send}),
      })
      .then(response => response.text())
      .then(message => alert(message))
      .catch(error => console.error('Error:', error));
    }
  }
}
