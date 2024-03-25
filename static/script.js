// Fade header image on scroll and remove the "Scroll to Generate" banner when the user scrolls down
const checkpoint = 300;
var banner = document.getElementById("banner");
var header_image = document.getElementById("header-image");
// var generate = document.getElementById("generate-button-container");
// var download = document.getElementById("download-button-container");
var instrument;
var chosen_instrument;
var chosen_tonality;
var tonality;
var tempo;
var key;
var checked = 0;

function start_functions() {
  checked = 0;
  // download.classList.add("hide");
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
      
      file_name = instrument_send + "_" + key_send + "_" + tonality_send + ".mid";
      alert("The song is being created!\nThis could take up to 15 minutes.");

      // generate.classList.add("hide");
      // download.classList.remove("hide");

      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/run-script', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.responseType = 'blob';

      xhr.onload = function() {
        if (this.status === 200) {
          var blob = this.response;
          var downloadLink = document.createElement('a');
          var url = window.URL.createObjectURL(blob);
          downloadLink.href = url;
          downloadLink.download = file_name;
          document.body.appendChild(downloadLink);
          downloadLink.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(downloadLink);
        }
      };
      xhr.send(JSON.stringify({instrument: instrument_send, tonality: tonality_send, tempo: tempo_send, key: key_send}));
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

      file_name = instrument_send + "_" + key_send + "_" + tonality_send + ".mid";

      alert("The song is being created!\nThis could take up to 15 minutes.");

      // generate.classList.add("hide");
      // download.classList.remove("hide");

      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/run-script', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.responseType = 'blob';

      xhr.onload = function() {
        if (this.status === 200) {
          var blob = this.response;
          var downloadLink = document.createElement('a');
          var url = window.URL.createObjectURL(blob);
          downloadLink.href = url;
          downloadLink.download = file_name;
          document.body.appendChild(downloadLink);
          downloadLink.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(downloadLink);
        }
      };
      xhr.send(JSON.stringify({instrument: instrument_send, tonality: tonality_send, tempo: tempo_send, key: key_send}));
    }
    else {
      console.log("1")
      var instrument_send = instrument_temp; 
      var tonality_send = tonality_temp; 
      var tempo_send = tempo_temp; 
      var key_send = get_key();

      console.log("instrument: ", instrument_send);
      console.log("tonality: ", tonality_send);
      console.log("tempo: ", tempo_send);
      console.log("key: ", key_send);

      file_name = instrument_send + "_" + key_send + "_" + tonality_send + ".mid";
      console.log("2")
      alert("The song is being created!\nThis could take up to 15 minutes.");
      console.log("3")
      // generate.classList.add("hide");
      // download.classList.remove("hide");

      var xhr = new XMLHttpRequest();
      console.log("4")
      xhr.open('POST', '/run-script', true);
      console.log("5")
      xhr.setRequestHeader('Content-Type', 'application/json');
      console.log("6")
      xhr.responseType = 'blob';
      console.log("7")

      xhr.onload = function() {
        if (this.status === 200) {
          console.log("8")
          var blob = this.response;
          var downloadLink = document.createElement('a');
          var url = window.URL.createObjectURL(blob);
          downloadLink.href = url;
          downloadLink.download = file_name;
          console.log("9")
          document.body.appendChild(downloadLink);
          downloadLink.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(downloadLink);
          console.log("10")
        }
      };
      console.log("11")
      xhr.send(JSON.stringify({instrument: instrument_send, tonality: tonality_send, tempo: tempo_send, key: key_send}));
      console.log("12")
    }
  }
}
