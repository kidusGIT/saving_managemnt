// UPDATE BUTTON
const update_member_btn = document.getElementById('update-member-btn');

// POP UP BUTTON
const popupBtn = document.getElementById('delete-member-btn');
const cancelPopupBtn = document.getElementById('cnacel-pop-up');
const deletePopupBtn = document.getElementById('delete-pop-up');
const popup_show = document.getElementById('pop-up-container')

// DELETE MEMBER
popupBtn.onclick = async (e) => {
    e.preventDefault()
    const response = await fetch(`http://${window.location.host}/members-api/check-balance/${member_id.value}`);
    const data = await response.json()
    console.log('status: ', data)
    const container = document.getElementById('error-container');
    const message = document.getElementById('error-message');

    if(data.delete){
        popup_show.classList.add('active');
        container.style.display = 'none'
        message.textContent = ""
    }  else {
        container.style.display = 'flex'
        message.textContent = "Memeber's Account balance Must Be Zero"
    }
    // popup_show.classList.add('active');
}

popup_show.onclick = () => {
    popup_show.classList.remove('active');

    
}

deletePopupBtn.onclick = async () => {
    
    const response = await fetch(`http://${window.location.host}/members-api/delete-member/${member_id.value}`);
    const data = await response.json()
    // const popup_show = document.getElementById('pop-up-container')
    popup_show.classList.remove('active');
    // window.location.replace(`http://${window.location.host}/members`)

    window.location.href = `http://${window.location.host}/members`;

        
}

cancelPopupBtn.onclick = () => {
    const popup_show = document.getElementById('pop-up-container')
    popup_show.classList.remove('active');
}

// VALIDATIONS
let firstNameCheck = 0, secondNameCheck = 0, lastNameCheck = 0, 
    phoneNumCheck = 0, emailCheck = 0, dateCheck = 0;

let hasError = false;

// UPDATE MEMBER
update_member_btn.onclick = async (e) => {
    e.preventDefault();

    // MEMBERS FORM
    const memberUpdateForm = document.getElementById('member-form-update');

    const myform = new FormData(memberUpdateForm);
    const values = [...myform.entries()]
    // values[10][1] :-- email
    // values[11][1] :-- age
    
    if(values[2][1] === '' || values[3][1] === '' || values[4][1] === '' || values[5][1] === '' || values[6][1] === '' ||
        values[7][1] === '' || values[9][1] === '' || values[10][1] === '') {
            console.log('all filds are required');
            container.style.display = 'flex'
            message.innerText = "all feilds are required"
            // accounts.disabled = false;                 
    } else {

        if(hasError) {
            container.style.display = 'flex'
            message.innerText = "all feilds are required"
        } else {
            const id = member_id.value;
            const response = await fetch(`/members-api/update-member/${id}`, {
                method:'PUT',
                headers:{
                    "X-CSRFToken": getCookie("csrftoken"),
                }, body: new FormData(memberUpdateForm),
            }); 

            const data = await response.json();
            
            if(data) {
                const message = document.getElementById('succuss-container')
                message.style.display = 'flex';
            }

        } 
    }         
}

// VALIDATION
const form_feilds = document.getElementsByTagName('input');

function validateName(name){
    if(name.match(/[0-9]+$/)){
        return 1;
    } 
    return 0;

}

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