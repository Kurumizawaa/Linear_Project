const api = "http://127.0.0.1:8000";

const urlParams = new URLSearchParams(window.location.search);
const searchname = urlParams.get('name')
const searchnameprompt = document.getElementById("searchnameprompt")
const searchnamesubmit = document.getElementById("searchnamesubmit")

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

async function showsearchname(){
    let headtext = document.getElementById("headtext")
    headtext.innerHTML = `<h1 class="m-0 mb-4 fw-semibold text-wrap text-light text-center" style="font-size: 50px ; max-width: 80vw;">Search results for : ${searchname}</h1>`
}

async function showgames(){
    console.log('name: ', searchname)
    let response = await fetch(`${api}/searchbyname?name=${searchname}`);
    let gamedata = await response.json();
    console.log(gamedata)
    let gamelist = document.getElementById("gamecard")
    let content = ""
    for (let i = 0; i < gamedata.length; i++){
        console.log(gamedata[i])
        let steamresponse = await fetch(`${api}/getsteam?gamename=${gamedata[i]['name']}`);
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
                <h2 class="card-title" style="font-size: 40px; font-family: 'd-din'; font-weight: bold;">${gamedata[i]['name']}</h2>
                <p class="card-text" style="font-family: 'd-din';">${gamedata[i]['description']}</p>
                <a href="${steamdata['steamlink']}" type="button" class="btn btn btn-outline-light me-2" style="font-family: 'd-din'; font-weight: bold;"><i class="bi bi-steam"></i>&nbsp;&nbsp;Steam</a>
            </div>
            </div>
        </div>
        </div>`
        gamelist.innerHTML = content
    }
}

function logname(){
    let prompt = searchnameprompt.value
    window.location.href = `byname.html?name=${prompt}`;
}

async function logout(){
    let response = await fetch(`${api}/logout`); // Fetch data from '/hotel' endpoint
    let data = await response.json(); // Parse the JSON response
    window.location.href = "index.html";
}

searchnamesubmit.addEventListener("click", logname)

show_btn_login();
showsearchname();
showgames();