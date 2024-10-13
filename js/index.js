const api = "http://127.0.0.1:8000";

const searchnameprompt = document.getElementById("searchnameprompt"); // Select the search bar input
const searchnamesubmit = document.getElementById("searchnamesubmit"); // Select the search button
const searchtagsubmit = document.getElementById("searchtagsubmit"); // Select the tag search button
const singletagsubmit = document.getElementById("singletagsubmit"); // Select the single tag search button

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

async function show_tag_select(){
  let response = await fetch(`${api}/gettags`); // Fetch data from '/hotel' endpoint
  let tag = await response.json(); // Parse the JSON response
  let selectsection = document.getElementById("tagselectform")
  let content = ""
  console.log(tag)
  for (const key of Object.keys(tag)){
    content += `<option value="${key}">${key}</option>`
  };
  selectsection.innerHTML = content
}

async function showgames(){
  let userresponse = await fetch(`${api}/currentuser`); // Fetch data from '/hotel' endpoint
  let userdata = await userresponse.json(); // Parse the JSON userresponse
  console.log(userdata)

  let gamelist = document.getElementById("gamecard")

  if(userdata != null){
    console.log('yes')
    let historyresponse = await fetch(`${api}/besthistorymatch`);
    let historydata = await historyresponse.json();
    console.log(historydata)
    if(historydata.length == 0){
      gamelist.innerHTML = `
      <div class="card mb-3" style="background-color: rgba(111, 111, 111, 0.25); border-color: aliceblue; border-width: 5px;">
        <div class="row g-0">
          <div class="col-md-4">
            <img src="/images/logobg.png" class="img-fluid rounded-5 p-2" alt="">
          </div>
          <div class="col-md-8">
            <div class="card-body" style="color: aliceblue;">
              <h2 class="card-title" style="font-size: 40px; font-family: 'd-din'; font-weight: bold;">Search history not found</h2>
              <p class="card-text" style="font-size: 20px; font-family: 'd-din';">Start Searching to get recommendations</p>
              <a onclick="scrollto('searchbytags-title')" type="button" class="btn btn btn-outline-light me-2" style="font-size: 20px; font-family: 'd-din'; font-weight: bold;">Go Search</a>
            </div>
          </div>
        </div>
      </div>
      `;     
    }
    else{
      let content = ""
      for (let i = 0; i < historydata.length; i++){
        console.log(historydata[i])
        let steamresponse = await fetch(`${api}/getsteam?gamename=${historydata[i]['name']}`);
        let steamdata = await steamresponse.json();
        console.log(steamdata['steamlink'])
        content += `
        <div class="card mb-3" style="background-color: rgba(111, 111, 111, 0.25); border-color: aliceblue; border-width: 5px;">
        <div class="row g-0">
            <div class="col-md-4">
            <img src="${steamdata['imgsrc']}" class="img-fluid rounded-5 p-2" alt="">
            </div>
            <div class="col-md-8">
            <div class="card-body" style="color: aliceblue;">
                <h2 class="card-title" style="font-size: 40px; font-family: 'd-din'; font-weight: bold;">${historydata[i]['name']}</h2>
                <p class="card-text" style="font-size: 20px; font-family: 'd-din';">${historydata[i]['description']}</p>
                <a href="${steamdata['steamlink']}" type="button" class="btn btn btn-outline-light me-2" style="font-size: 20px; font-family: 'd-din'; font-weight: bold;"><i class="bi bi-steam"></i>&nbsp;&nbsp;Steam</a>
            </div>
            </div>
        </div>
        </div>`
        gamelist.innerHTML = content
    }
    }
  }
  else{
    console.log('no')
    gamelist.innerHTML = `
            <div class="card mb-3" style="background-color: rgba(111, 111, 111, 0.25); border-color: aliceblue; border-width: 5px;">
              <div class="row g-0">
                <div class="col-md-4">
                  <img src="/images/logobg.png" class="img-fluid rounded-5 p-2" alt="">
                </div>
                <div class="col-md-8">
                  <div class="card-body" style="color: aliceblue;">
                    <h2 class="card-title" style="font-size: 40px; font-family: 'd-din'; font-weight: bold;">Please Log in</h2>
                    <p class="card-text" style="font-size: 20px; font-family: 'd-din';">Log in to save search history</p>
                    <a href="login.html" type="button" class="btn btn btn-outline-light me-2" style="font-size: 20px; font-family: 'd-din'; font-weight: bold;">Log in</a>
                  </div>
                </div>
              </div>
            </div>
    `;
  }
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

function logsingletag() {
  let selectBox = document.getElementById("tagselectform");
  let tag = selectBox.value;
  console.log(tag)

  let singleplayer = document.getElementById("singleplayer-singletag");
  let multiplayer = document.getElementById("multiplayer-singletag");

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

  window.location.href = `tagsearch.html?tag=${tag}&playertype=${playertype}`;
}

function logname(){
  let prompt = searchnameprompt.value
  window.location.href = `byname.html?name=${prompt}`;
}

function scrollto(element){
  document.getElementById(element).scrollIntoView()
}

show_btn_login();
show_tag_checkbox();
show_tag_select();
showgames();

searchnamesubmit.addEventListener("click", logname);
searchtagsubmit.addEventListener("click", logtag);
singletagsubmit.addEventListener("click", logsingletag);

//// Template ///
// const searchnameprompt = document.getElementById("searchnameprompt"); // Select the search bar input
// const searchnamesubmit = document.getElementById("searchnamesubmit"); // Select the search button

// function logname(){
//   let prompt = searchnameprompt.value
//   window.location.href = `byname.html?name=${prompt}`;
// }


// searchnamesubmit.addEventListener("click", logname);