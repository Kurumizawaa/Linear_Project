const api = "http://127.0.0.1:8000";

const searchnameprompt = document.getElementById("searchnameprompt"); // Select the search bar input
const searchnamesubmit = document.getElementById("searchnamesubmit"); // Select the search button
const searchtagsubmit = document.getElementById("searchtagsubmit"); // Select the tag search button

async function show_btn_login(){
  let response = await fetch(`${api}/currentuser`); // Fetch data from '/hotel' endpoint
  let userdata = await response.json(); // Parse the JSON response
  console.log(userdata)
  
  if(userdata != null){
      let user = document.getElementById("login_user");
      user.innerHTML = `<a href="#"><button type="button" class="btn btn btn-outline-light me-2">${userdata['username']}</button></a>
                        <a><button id="logout-button" type="button" class="btn btn btn-light">Log Out</button></a>`
      logoutbutton = document.getElementById("logout-button")
      logoutbutton.addEventListener("click", logout)
  }
}

async function logout(){
  let response = await fetch(`${api}/logout`); // Fetch data from '/hotel' endpoint
  let data = await response.json(); // Parse the JSON response
  window.location.href = "index.html";
}

async function show_tag_checkbox(){
  let response = await fetch(`${api}/gettags`); // Fetch data from '/hotel' endpoint
  let tags = await response.json(); // Parse the JSON response
  let checkboxsection = document.getElementById("tagcheckbox")
  let content = ""
  console.log(tags)
  for (const key of Object.keys(tags)){
    content += `
            <div class="form-check col-4 mb-3">
              <input class="form-check-input" type="checkbox" value="" id="${key}">
              <label class="form-check-label fs-4" for="${key}">${key}</label>
            </div>`
  };
  checkboxsection.innerHTML = content
}

function logtag() {
  let tagCheckboxes = document.querySelectorAll("#tagcheckbox input[type='checkbox']");

  let tags = Array.from(tagCheckboxes).map(checkbox => checkbox.checked ? '1' : '0').join('');

  let singleplayer = document.getElementById("singleplayer");
  let multiplayer = document.getElementById("multiplayer");

  let playertype;
  if ((singleplayer.checked && multiplayer.checked) || (!singleplayer.checked && !multiplayer.checked)) {
    playertype = "mixed"; // Both selected
  } else if (singleplayer.checked) {
    playertype = "single"; // Only singleplayer selected
  } else if (multiplayer.checked) {
    playertype = "multi"; // Only multiplayer selected
  } else {
    playertype = "mixed"; // Neither selected
  }

  window.location.href = `bytags.html?tags=${tags}&playertype=${playertype}`;
}


function scrollto(element){
  document.getElementById(element).scrollIntoView()
}

function lognormal(){
  console.log("Fuck you")
}


show_btn_login();
show_tag_checkbox();

searchnamesubmit.addEventListener("click", lognormal);
searchtagsubmit.addEventListener("click", logtag);
