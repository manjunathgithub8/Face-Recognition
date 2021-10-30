 function call_python() {
    eel.call_camera()();
    document.getElementById("stop-icon").style.display = "none";
    document.getElementById("syn").innerHTML=''
    document.getElementById("record-icon").style.display = "block";
	  document.getElementById("st").innerHTML='Camera Running'
}

eel.expose(returned_face);
function returned_face(face_name) {
    var curr=document.getElementById('list-wrapper')
    curr.innerHTML='';
    for (var prop in face_name) {
      curr.innerHTML += '<li class="list-group-item">' + face_name[prop] + '</li>';
     
    }
    }
  
function list_click() {    
  eel.givetodaylist()();
}

eel.expose(today_list);
function today_list(list_entry) {
    console.log(list_entry);
    var currtoday=document.getElementById('list-wrapper-today')
    currtoday.innerHTML='';
    
    for (var obj in list_entry) {
        currtoday.innerHTML += '<tr><td>' +obj+'</td><td >' +list_entry[obj]+ '</td></tr>';  
    }
    }


  function testsync() {
    eel.StopStream()();
    document.getElementById("st").innerHTML=''
    document.getElementById("record-icon").style.display = "none";
    document.getElementById("stop-icon").style.display = "block";
	  document.getElementById("syn").innerHTML='Ended'
}

//dashboard
function dashboard_view()
{
  eel.opendash()();
  console.log('entered');
}


//login

const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("submit-btn");
if(loginButton){
  loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.email.value;
  const password = loginForm.password.value;
  eel.verify_Login(username,password)
    
})
}

eel.expose(login_auth);
function login_auth(rkey)
{
  if (rkey==true){
    window.location="home.html";
  }
  else{
    alert("Wrong Details!")
  }
}


//menu list

const adduserbtn=document.getElementById("adduserbtn");
droplist=document.getElementById("deptselect");
droplist.innerHTML="<option selected>Select</option>";
adduserbtn.addEventListener("click", (ue)=>{
  eel.givedeptlist()();  
})


eel.expose(dispdept);
function dispdept(deptlist)
{
  //console.log(deptlist);
  let list = document.getElementById("deptselect");
  list.innerHTML="<option selected>Select</option>";
  deptlist.forEach((item) => {
    list.innerHTML+=`<option value="${item}">${item}</option>`;
  });
}


//add Employee

const adduserButton = document.getElementById("submit-user");
adduserButton.addEventListener("click", (ue)=>{
    ue.preventDefault();
    var inputs = document.querySelectorAll("#add-user input,select");
    mod_cont=document.getElementById('modal-body');
    mod_cont.innerHTML='<div class="alert alert-dark" role="alert">Please wait till Image is Encoded and uploaded!</div><div class="loader"><svg class="circular" viewBox="25 25 50 50"><circle class="path" cx="50" cy="50" r="20" fill="none" stroke-width="2" stroke-miterlimit="10"/></svg></div>';
    eel.adduser(inputs[0].value,inputs[1].value,inputs[2].value)();
    
}) 
preform=document.getElementById('modal-body').innerHTML;
eel.expose(updateuser);
function updateuser(value1){
  mod_cont=document.getElementById('modal-body');
  if (value1==true){
    contentmsg='<div class="alert alert-success" role="alert">Added User Successfully!</div>';
  }
  else{
    contentmsg='<div class="alert alert-danger" role="alert">Retry Adding User!</div>';
  }
  mod_cont.innerHTML=contentmsg;
  setTimeout(function(){
    mod_cont.innerHTML=preform;
    $('#adduser').modal('hide');
  }, 3000);
  
  
}


//logout
const logoutButton = document.getElementById("logout");
if(logoutButton){
  logoutButton.addEventListener("click", (e) => {
  window.location='login.html';
  })
}
