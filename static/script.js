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
    alert("Please select all parameters.\n\nOtherwise on the next click of the \"Generate\" button, the program will default to: \n\nInstrument: Piano\nTonality: Major\nTempo: 120 bpm\nLength: 1 minute");
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
      // console.log(instrument);
      var instrument_send = instrument; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'instrument': instrument_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      }); 
      // console.log(tonality);
      var tonality_send = tonality; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'tonality': tonality_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      }); 
      // console.log(tempo);
      var tempo_send = tempo; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'tempo': tempo_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      }); 
      // console.log(length);
      var length_send = length; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'length': length_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
    }
    else {
      set_tempo(120);
      set_length(1);
    }
  } else {
    if (double_check_if_all_chosen()) {
      // console.log(instrument);
      var instrument_send = instrument; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'instrument': instrument_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
      // console.log(tonality);
      var tonality_send = tonality; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'tonality': tonality_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      }); 
      // console.log(tempo);
      var tempo_send = tempo; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'tempo': tempo_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
      // console.log(length);
      var length_send = length; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'length': length_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
    }
    else {
      // console.log(instrument_temp);
      var instrument_send = instrument_temp; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'instrument': instrument_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
      // console.log(tonality_temp);
      var tonality_send = tonality_temp; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'tonality': tonality_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      }); 
      set_tempo(120);
      // console.log(tempo);
      var tempo_send = tempo; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'tempo': tempo_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
      set_length(1);
      // console.log(length);
      var length_send = length; 
      $.ajax({ 
          url: '/process', 
          type: 'POST', 
          contentType: 'application/json', 
          data: JSON.stringify({ 'length': length_send }), 
          success: function(response) { 
              document.getElementById('output').innerHTML = response.result; 
          }, 
          error: function(error) { 
              console.log(error); 
          } 
      });
    }
  }
}