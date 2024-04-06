// LIST FORM
const list_form = document.getElementById('list-form')
const list_btn = document.getElementById('list-btn')
const set_form = document.getElementById('set-form')

// OTHER BUTTONS
const change_count = document.getElementById('change-accunt-count')
const change_has_saved = document.getElementById('change-has-saved')
const set_dates = document.getElementById('set-btn')

// SET DATE FORM
const set_btn = document.getElementById('set-btn')

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

list_btn.onclick = async (e) => {
    e.preventDefault()

    change_count.style.display = 'block'
    change_has_saved.style.display = 'block'

    const data = await getMembers()
    setComponents(data);

}

const getMembers = async () => {
    const response = await fetch(`http://${window.location.host}/supervisors/member-savings`, {
        method:'POST',
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
        }, body: new FormData(list_form),
    })

    const data = await response.json()
    return data
}

const setComponents = (data) => {
    const membersList = document.getElementById('tabel')

    const header = `
        <tr>
            <th> Member's ID </th>
            <th> Member's name </th>
            <th> father name </th>
            <th> Grand father name </th>
            <th> Email </th>
            <th> Missed Saving </th>
        </tr>
    `
    let lists = ``
    for(let d in data){
        let list = `
            <tr>
                <td> ${data[d].member_id} </td>
                <td> ${data[d].first_name} </td>
                <td> ${data[d].father_name} </td>
                <td> ${data[d].garnd_father_name} </td>
                <td> ${data[d].email} </td>
                <td class="withdraw" > ${data[d].save_count * 500 } ETB </td>
            </tr>
        `

        lists += list
    }

    const concat = header + lists
    membersList.innerHTML = concat

    set_form.style.display = 'flex'
}

change_count.onclick = async () => {
    const response = await fetch(`http://${window.location.host}/supervisors/change-save-account`)
    const data = await getMembers()
    setComponents(data);
}

change_has_saved.onclick = async () => {
    const response = await fetch(`http://${window.location.host}/supervisors/check-has-saved`);
    const data = await response.json();
}

set_btn.onclick = async (e) => {
    e.preventDefault()
    const response = await fetch(`http://${window.location.host}/supervisors/set-time`, {
        method:'POST',
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
        }, body: new FormData(set_form),
    })

    location.reload();
}
