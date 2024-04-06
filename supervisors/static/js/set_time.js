
// SET DATE FORM
const set_form = document.getElementById('set-form')
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