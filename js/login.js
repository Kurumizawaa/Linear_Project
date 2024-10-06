const api = "http://127.0.0.1:8000";

inputusername = document.getElementById("login-username")
inputpassword = document.getElementById("login-password")
loginbutton = document.getElementById("login-button")

async function checkuser(){
  let response = await fetch(`${api}/currentuser`); // Fetch data from '/hotel' endpoint
  let userdata = await response.json(); // Parse the JSON response
  console.log("user: ", userdata)
  
  if(userdata != null){
    window.location.href = `index.html`;
  }
}

async function login(){
    const user_name = inputusername.value.trim();
    const user_password = inputpassword.value.trim();

    if(user_name === '' || user_password === ''){
        alert("Please enter Username / password");
        return;
    }
    try{
        const response = await fetch(`${api}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: user_name,
                password: user_password
            })
        });
        if(response.ok) {
            const data = await response.json();
            if(data) {
                window.location.href = "index.html";
            }
            else {
                alert("Login failed. Please check your credentials.");
            }
        }
        else {
            const errorMessage = await response.text();
            alert("Login Failed: " + errorMessage);
        }
    }    
    catch(error) {
        console.error('Error:', error);
        alert("Incorrect Username or Password");
    }
}

async function logincheck(){
    console.log(inputusername.value)
    console.log(inputpassword.value)
}

loginbutton.addEventListener("click", login);

checkuser()