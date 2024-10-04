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
                        <a href="#"><button type="button" class="btn btn btn-light">Log Out</button></a>`
  }
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
              <label class="form-check-label fs-4" for="defaulttagcheck">${key}</label>
            </div>`
  };
  checkboxsection.innerHTML = content
}

function scrollto(element){
  document.getElementById(element).scrollIntoView()
}

function lognormal(){
  console.log("Fuck you")
}
function logtag(){
  console.log("Fuck you, but in Tag")
}


show_btn_login();
show_tag_checkbox();

searchnamesubmit.addEventListener("click", lognormal);
searchtagsubmit.addEventListener("click", logtag);
