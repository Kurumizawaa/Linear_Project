const api = "http://127.0.0.1:8000";

inputusername = document.getElementById("signup-username")
inputpassword = document.getElementById("signup-password")
inputpasswordconfirm = document.getElementById("signup-passwordconfirm")
signupbutton = document.getElementById("signup-button")

async function checkuser(){
  let response = await fetch(`${api}/currentuser`); // Fetch data from '/hotel' endpoint
  let userdata = await response.json(); // Parse the JSON response
  console.log("user: ", userdata)
  
  if(userdata != null){
    window.location.href = `index.html`;
  }
}

async function signup(){
    const user_name = inputusername.value.trim();
    const user_password = inputpassword.value.trim();
    const user_passwordconfirm = inputpasswordconfirm.value.trim();

    if(user_name === '' || user_password === '' || user_passwordconfirm === ''){
        alert("Please enter Username / password");
        return;
    }
    if(user_password != user_passwordconfirm){
        alert("Password doesn't match");
        return;
    }
    try{
        const response = await fetch(`${api}/signup`, {
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
                alert("Register failed. Please check your credentials.");
            }
        }
        else {
            const errorMessage = await response.text();
            alert("Register Failed: " + errorMessage);
        }
    }    
    catch(error) {
        console.error('Error:', error);
        alert("Error");
    }
}

signupbutton.addEventListener("click", signup);

checkuser()