function getAge(date) {
  const currentDate = new Date().getFullYear();

  const dob = new Date(date).getFullYear();
  const age = currentDate - dob;

  return age;
}

function getDate(date) {
  const createDate = new Date(date).toLocaleDateString();

  return createDate;
}

function createTable(list) {
  let concat = `
        <tr> 
            <th> Memeber ID </th> 
            <th> Full Name </th> 
            <th> Email </th> 
            <th> Phone Number </th> 
            <th> Age </th> 
            <th> Created Date </th> 
            <th> Has Saved </th> 
        </tr>
    `;

  const table = document.getElementById("members-list-table");

  for (let i in list) {
    let data = `
            <tr >
                <td> <a href="http://${
                  window.location.host
                }/members/memeber-info/${
      list[i].member_id
    }" class="member-detail"> ${list[i].member_id} </a> </td>
                <td> ${list[i].first_name} ${list[i].father_name}  ${
      list[i].garnd_father_name
    }  </td>
                <td> ${list[i].email} </td>
                <td> ${list[i].phone_num} </td>
                <td> ${getAge(list[i].age)} </td>
                <td> ${getDate(list[i].created_date)} </td>
                <td> ${
                  list[i].has_saved
                    ? '<i class="fa-solid fa-circle-check"></i> '
                    : '<i class="fa-solid fa-circle-xmark">'
                } </td>
            </tr>
        `;
    concat += data;
  }

  table.innerHTML = concat;
  const empty = document.getElementById("noting-found");
  empty.style.display = "none";
}

async function members_list() {
  const response = await fetch(
    `http://${window.location.host}/members-api/member-list/`
  );

  const list = await response.json();
  createTable(list);
}

members_list();

const search_input = document.getElementById("search-input");
const search_btn = document.getElementById("search-btn");

function displayEmpty() {
  const empty = document.getElementById("noting-found");
  empty.style.display = "flex";
}

search_input.onchange = async (e) => {
  if (e.target.value == "") {
    members_list();
  }

  if (e.target.value != "") {
    const response = await fetch(
      `http://${window.location.host}/members-api/search_member/?search=${e.target.value}`
    );

    const data = await response.json();
    createTable(data);
    if (data.length == 0) {
      displayEmpty();
    }
  }
};

search_btn.onclick = async (e) => {
  const searchData = search_input.value;
  const response = await fetch(
    `http://${window.location.host}/members-api/search_member/?search=${searchData}`
  );

  const data = await response.json();
  createTable(data);
  if (data.length == 0) {
    displayEmpty();
  }
};
