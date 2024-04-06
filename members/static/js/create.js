// FORMS
const memberForm = document.getElementById('create-member-form');
const compulsoryForm = document.getElementById('compulsory-form');
const savingForm = document.getElementById('saving-form');

//FORM BUTTONS
const create_member = document.getElementById('create-member-btn');
const create_compulsory_account = document.getElementById('create-compulosry-account');
const create_saving_account = document.getElementById('create-saving-account');

// BUTTONS
const accounts = document.getElementById('accounts');
const member = document.getElementById('member');

// DIVS
const account_holder = document.getElementById('account-holder');
const member_holder = document.getElementById('member-holder');

// INPUTS
const member_id = document.getElementById('member_id');
const compulsory_id = document.getElementById('compulsory-acctount-id');
const saving_id = document.getElementById('saving-acctount-id');

// INPUTS FOR TRANSACTION
const compulsory_balance = document.getElementById('saving-acct-balance');
const saving_balance = document.getElementById('com-acct-balance');

compulsory_balance.onchange = (e) => {
    if(e.target.value == ""){
        create_saving_account.style.display = 'none'

    } else {
        create_saving_account.style.display = 'block'

    }
}

saving_balance.onchange = (e) => {
    console.log('changed')
    if(e.target.value == ""){
        create_compulsory_account.style.display = 'none'
        
    } else if (e.target.value >= 500 ) {
        create_compulsory_account.style.display = 'block'
        
    } else if(e.target.value < 500) {
        create_compulsory_account.style.display = 'none'

    } else {
        create_compulsory_account.style.display = 'block'

    }
}


// TOP BUTTONS EVENTS
accounts.onclick = () => {
    account_holder.style.display = 'flex';
    member_holder.style.display = 'none';
}

member.onclick = () =>{
    account_holder.style.display = 'none';
    member_holder.style.display = 'flex';
}
        
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// VALIDATIONS
let firstNameCheck = 0, secondNameCheck = 0, lastNameCheck = 0, 
    phoneNumCheck = 0, emailCheck = 0, dateCheck = 0;

let hasError = false;

// FORMS 
create_member.onclick = async (e) => {
    e.preventDefault();
    const myform = new FormData(memberForm);

    const values = [...myform.entries()]

    if(values[1][1] === '' || values[2][1] === '' || values[3][1] === '' || values[4][1] === '' || values[5][1] === '' ||
        values[6][1] === '' || values[8][1] === '' || values[9][1] === '' || values[10][1] === '') {
            console.log('all filds are required');
            container.style.display = 'flex'
            message.innerText = "all feilds are required"

    } else {
        
        if(hasError){
            container.style.display = 'flex'
            message.innerText = "all feilds are required"
        } else {
            
            container.style.display = 'none'
            message.innerText = ""

            const response = await fetch(`http://${window.location.host}/members-api/create-member/`, {
                method:'POST',
                headers:{
                    "X-CSRFToken": getCookie("csrftoken"),
                }, body: new FormData(memberForm),
            }); 

            const data = await response.json();
            
            if(data) {
                account_holder.style.display = 'flex';
                member_holder.style.display = 'none';
                accounts.disabled = false;
            }
        }
    }
}

// compulsory saving 
create_compulsory_account.onclick = async (e) => {
    e.preventDefault();
    
    const response = await fetch(`http://${window.location.host}/savings-api/create-account/${member_id.value}`, {
        method:'POST',
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
        }, body: new FormData(compulsoryForm),
    }); 

    const data = await response.json();
    
    if(data) {
        const createContainer = document.getElementById('create-container');
        const createMessage = document.getElementById('create-message');

        createContainer.style.display = 'flex';
        createMessage.innerText = "Compulsory Account Created";
    }
    
}

// OTHERS SAVING 
create_saving_account.onclick = async (e) => {
    e.preventDefault();

    const response = await fetch(`http://${window.location.host}/savings-api/create-saving-account/${member_id.value}`, {
        method:'POST',
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
        }, body: new FormData(savingForm),
    }); 

    const data = await response.json();
    if(data) {
        const createContainer = document.getElementById('create-container');
        const createMessage = document.getElementById('create-message');

        createContainer.style.display = 'flex';
        createMessage.innerText = "Saving Account Created";
    }    
}

const form_feilds = document.getElementsByTagName('input');

function validateName(name){
    if(name.match(/[0-9]+$/)){
        return 1;
    } 
    return 0;

}

// VALIDATION
const container = document.getElementById('error-container');
const message = document.getElementById('error-message');
let previousError = '';

const checkValidation = (text) => {
    if(firstNameCheck === 1 || secondNameCheck === 1 || lastNameCheck === 1 || phoneNumCheck === 1 
        || emailCheck === 1 || dateCheck === 1 ){
        container.style.display = 'flex';

        if(text === '') {
            message.innerText = previousError;
            console.log('previous: ', previousError)
            console.log('text: ', text)
        } else {
            message.innerText = text;
            previousError = text;
        }
        
        hasError = true;
    } else {
        container.style.display = 'none'
        message.innerText = ""
        hasError = false;
    }
}

form_feilds[1].onchange = (e) => {
    if(validateName(e.target.value) == 1) {

        firstNameCheck = 1;

        checkValidation("Only Numbers Are Allowed On This Feild")
    } else{

        firstNameCheck = 0;
        checkValidation("")
    }
    
}
form_feilds[2].onchange = (e) => {
    if(validateName(e.target.value) == 1) {

        secondNameCheck = 1;
        checkValidation("Only Numbers Are Allowed On This Feild");
    } else{

        secondNameCheck = 0;
        checkValidation("")
    }
    
}
form_feilds[3].onchange = (e) => {
    if(validateName(e.target.value) == 1) {

        lastNameCheck = 1;
        checkValidation("Only Numbers Are Allowed On This Feild");

    } else{

        lastNameCheck = 0;
        checkValidation("")
    }
}

// phone number validation
form_feilds[8].onchange = (e) => {
    console.log(e.target.value)
    const number = e.target.value;

    if(number.length < 10) {

        phoneNumCheck = 1;
        checkValidation("Phone Number Must Have 10 Digits");
    } else if (number.length > 10) {

        phoneNumCheck = 1;
        checkValidation("Phone Number Must Have 10 Digits");
    } else if(number.length === 10) {
        phoneNumCheck = 0;
        checkValidation("")
    }

}

// email address validation
form_feilds[9].onchange = (e) => {
    const email = e.target.value;

    if(!email.includes('@') || !email.includes('.')) {
        emailCheck = 1;

        checkValidation("Email Must Contain '.' or '@' ");
    } else {
        emailCheck = 0;      
        checkValidation("")
    }
}

// date of birth validation
form_feilds[10].onchange = (e) => {
    const date = e.target.value;
    const dob = new Date(date).getFullYear();

    const currentDate = new Date().getFullYear();
      
    const age = currentDate - dob
    
    if(age < 18){
        dateCheck = 1;

        checkValidation("Member Is Under Age");
    } else {
        dateCheck = 0;
        checkValidation("")
    }
    
}