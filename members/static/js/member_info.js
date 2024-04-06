// FORMS
const memberUpdateForm = document.getElementById('member-form-update');
const compulsorySavingUpdateForm = document.getElementById('compulsory-saving-update-form');
const savingUpdateForm = document.getElementById('saving-update-form');

// BUTTONS
const member_btn = document.getElementById('member');
const accounts_btn = document.getElementById('accounts');
const transactions_btn = document.getElementById('transactions');
const change_account = document.getElementById('change-account');

// FORM BUTTONS
const update_compulosry_btn = document.getElementById('update-compulosry-account');
const update_saving_btn = document.getElementById('update-saving-account');

// DIV'S
const update_form = document.getElementById('update-form');
const account_holder = document.getElementById('account-holder');
const transactions_div = document.getElementById('transactions-div');

// INPUTS 
const member_id = document.getElementById('member_id');
const active_account = document.getElementById('active-account');

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

// TOP BUTTONS
member_btn.onclick = () => {
    console.log('member')
    account_holder.style.display = 'none'
    update_form.style.display = 'flex'
    transactions_div.style.display = 'none'
}

accounts_btn.onclick = () => {
    account_holder.style.display = 'flex'
    update_form.style.display = 'none'
    transactions_div.style.display = 'none'

    getAccounts();
}

transactions_btn.onclick = () => {
    account_holder.style.display = 'none'
    update_form.style.display = 'none'
    transactions_div.style.display = 'flex'

    const saving_id = document.getElementById('saving_account_id');
    const active = active_account.value;
    saving_id.value = active
    
    setBalance()
}

const setBalance = async () => {
    const compulsory_balance = document.getElementById('compulsory_balance');
    const saving_balance = document.getElementById('saving_balance');

    const id = member_id.value;

    const active = active_account.value;
    const compulsoryResponse = await fetch(`http://${window.location.host}/savings-api/compulsory-detail/${id}`);
    const compulsory = await compulsoryResponse.json()

    const savingResponse = await fetch(`http://${window.location.host}/savings-api/saving-account-detail/${active}`);
    const savings = await savingResponse.json()
    
    compulsory_balance.innerHTML =  `Balance: ${compulsory.balance}` 

    saving_balance.innerHTML = `Balance: ${savings.balance}`

    if(savings.is_suspended){
        savingWithdraw.disabled = true
        
    } else {
        savingWithdraw.disabled = false

    }

    if(compulsory.is_suspended){
        compulsoryWithdraw.disabled = true
        
    } else {
        compulsoryWithdraw.disabled = false

    }
}
const changeAccount = async (account_id) => {
    const active = active_account.value;
            
    const response = await fetch(`http://${window.location.host}/savings-api/change-saving-account/${account_id}/${active}`); 

    const data = response.status;
    if(data === 200){
        getAccounts()
        // setCreateAccount()
    }
}

async function setId() {
    const response = await fetch(`http://${window.location.host}/savings-api/get-id`); 

    const data = await response.json()
    const acct_id = document.getElementById('saving-acct-id');
    acct_id.value = data.id

}

// SAVING ACCOUNT
update_saving_btn.onclick = async (e) => {
    e.preventDefault();
    // for change 0
    // for new account 1
    const active = active_account.value;

    const response = await fetch(`http://${window.location.host}/savings-api/update-account/${member_id.value}/${active}`, {
        method:'POST',
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
        }, body: new FormData(savingUpdateForm),
    }); 

    const data = response.status;
    if(data === 200){
        getAccounts()
        setCreateAccount()
        setId();
    }
}

// CREATE ACCOUNTS
async function setCreateAccount(){
    const combo_list = document.getElementById('saving_type');
    const saving_id = document.getElementById('saving_account');

    const accounts = await getMemberSaving()
    const response = await fetch(`http://${window.location.host}/savings-api/account-type`);
    const account_types = await response.json()


    // MEMBERS ACCOUNT
    const membersAccounts = []
    for(let account in accounts){
        membersAccounts.push(accounts[account].saving_type.account_name)
    }

    if(membersAccounts.length !== 4){
        savingUpdateForm.style.display = 'flex'  
        
        const not_created = []            
        for(let account in account_types){
            if(!membersAccounts.includes(account_types[account].account_name)){
                not_created.push(account_types[account])
            } 
        }  
        
        let lists = ``
        for(let i in not_created){
            let list = `
                <option value="${not_created[i].id}"> ${not_created[i].account_name} </option>
            `
            lists += list
        }

        combo_list.innerHTML = lists
    } else{
        savingUpdateForm.style.display = 'none'
    }

}

setCreateAccount();
// CREATE ACCOUNTS ENDS
async function getMemberSaving(){
    const id = member_id.value;
    const response = await fetch(`http://${window.location.host}/savings-api/member-savings/${id}`);
    const data = await response.json()

    return data
}

async function getAccounts(){
    const saving_lists = document.getElementById('saving-lists');

    const data = await getMemberSaving();
    let lists = ``
    for(let d in data){

        if(data[d].is_active){
            active_account.value = data[d].account_id;

            let list = `
                <div class="active-status">
                    <span>
                        <p> Account ID ${data[d].account_id} </p>
                        <p> ${data[d].saving_type.account_name}  </p>
                    </span>
                    <p> Balance ${data[d].balance} </p>
            
                </div> 
            `
            lists += list;
        } else {
            let list = `
                <div class="unactive-status">
                    <span class="unactive-status-span">
                        <p> Account ID ${data[d].account_id} </p>
                        <p> ${data[d].saving_type.account_name} </p>
                    </span>
                    <span class="unactive-status-span-2">
                        <button class="change-account-btn" id="id-${data[d].account_id}" onclick="changeAccount(${data[d].account_id})"> Change </button>
                    </span>
                </div> 
            `
            lists += list;
        }

    }

    saving_lists.innerHTML = lists;

}

getAccounts();
