// Fade header image on scroll and remove the "Scroll to Generate" banner when the user scrolls down
const checkpoint = 300;
var banner = document.getElementById("banner");
var header_image = document.getElementById("header-image");
var instrument;
var chosen_instrument;
var chosen_tonality;
var tonality;
var tempo;
var length = 0;
var key;
var checked = 0;

window.addEventListener("scroll", () => {
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

function choose_tonality(tonality) {
  this.tonality = tonality
  chosen_tonality = tonality
}

function get_tempo() {
  this.tempo = document.getElementById("slider-text").innerHTML;
  return tempo;
}

function set_tempo(tempo) {
  this.tempo = tempo;
}

function get_length() {
  this.length = document.getElementById("length-input").value;
  if (length == null) {
    length = 0;
  }
  return length;
}

function set_length(length) {
  this.length = length;
}

function check_if_all_chosen() {
  if (chosen_instrument == null || chosen_tonality == null || tempo == null || length == 0) {
    alert("Please select all parameters.\n\nOtherwise the program will default to: \nInstrument: Piano\nTonality: Major\nTempo: 120 bpm\nLength: 1 minute");
    this.checked = 1;
    return false;
  }
  return true;
}

function double_check_if_all_chosen() {
  if (chosen_instrument == null || chosen_tonality == null || tempo == null || length == 0) {
    return false;
  }
  return true;
}

function send_parameters() {
  instrument = chosen_instrument;
  tonality = chosen_tonality;
  var instrument_temp = "piano";
  var tonality_temp = "major";
  tempo = get_tempo();
  length = get_length();
  
  if (checked == 0) {
    if (check_if_all_chosen()) {
      console.log(instrument);
      console.log(tonality);
      console.log(tempo);
      console.log(length);
    }
    else {
      console.log(instrument_temp);
      console.log(tonality_temp);
      set_tempo(120);
      console.log(tempo);
      set_length(1);
      console.log(length);
    }
  } else {
    if (double_check_if_all_chosen()) {
      console.log(instrument);
      console.log(tonality);
      console.log(tempo);
      console.log(length);
    }
    else {
      console.log(instrument_temp);
      console.log(tonality_temp);
      set_tempo(120);
      console.log(tempo);
      set_length(1);
      console.log(length);
    }
  }
}