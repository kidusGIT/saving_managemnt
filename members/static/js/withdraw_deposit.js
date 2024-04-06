//  DEPOSIT AND WITHDRAW
const compulsoryDeposit = document.getElementById("compulsory-account-deposit");
const compulsoryWithdraw = document.getElementById(
  "compulsory-account-withdraw"
);

const savingDeposit = document.getElementById("saving-account-deposit");
const savingWithdraw = document.getElementById("saving-account-withdraw");

// INPUTS
const compulosry_input = document.getElementById("compulsory-balance");
const saving_input = document.getElementById("saving-balance");

// TEXT
const withdraw_err = document.getElementById("withdraw-error");

compulosry_input.onchange = (e) => {
  const saving_withdraw_btn = document.getElementById(
    "saving-account-withdraw"
  );
  const compulsory_withdraw_btn = document.getElementById(
    "compulsory-account-withdraw"
  );

  const compulsory_deposit_btn = document.getElementById(
    "compulsory-account-deposit"
  );
  // const saving_deposit_btn = document.getElementById('saving-account-deposit')

  if (e.target.value == "") {
    compulsory_withdraw_btn.style.display = "none";
    // saving_deposit_btn.style.display = 'none'
    compulsory_deposit_btn.style.display = "none";
  } else {
    compulsory_withdraw_btn.style.display = "block";
    withdraw_err.style.display = "none";
  }
};

saving_input.onchange = (e) => {
  const saving_withdraw_btn = document.getElementById(
    "saving-account-withdraw"
  );
  const compulsory_withdraw_btn = document.getElementById(
    "compulsory-account-withdraw"
  );

  // const compulsory_deposit_btn = document.getElementById('compulsory-account-deposit')
  const saving_deposit_btn = document.getElementById("saving-account-deposit");

  if (e.target.value == "") {
    saving_withdraw_btn.style.display = "none";
    compulsory_withdraw_btn.style.display = "none";

    saving_deposit_btn.style.display = "none";
    // compulsory_deposit_btn.style.display = 'none'
  } else {
    saving_withdraw_btn.style.display = "block";
  }
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// WITHDRAW AND DEPOSIT FOR COMPULSORY
compulsoryDeposit.onclick = async (e) => {
  e.preventDefault();
  console.log("cliked");

  const id = document.getElementById("compusory_account_id");
  const compolsory_saving_form = document.getElementById(
    "compolsory_saving_form"
  );

  const member_id = document.getElementById("member_id");

  const response = await fetch(
    `http://${window.location.host}/savings-api/deposit-to-compulosry/${id.value}/${member_id.value}`,
    {
      method: "PUT",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: new FormData(compolsory_saving_form),
    }
  );

  const status = response.status;
  const data = await response.json();
  if (status === 200) {
    const indicator = document.getElementById("deposit-withdraw-indicator");
    indicator.classList.remove("withdraw-indicator");
    indicator.classList.add("deposit-indicator");
    indicator.textContent = "The amount is deposited successfully";
    setBalance();
  } else {
    console.log();
  }
  console.log(data);
};

compulsoryWithdraw.onclick = async (e) => {
  e.preventDefault();
  const id = document.getElementById("compusory_account_id");
  const compolsory_saving_form = document.getElementById(
    "compolsory_saving_form"
  );

  const response = await fetch(
    `http://${window.location.host}/savings-api/withdraw-to-compulosry/${id.value}`,
    {
      method: "PUT",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: new FormData(compolsory_saving_form),
    }
  );

  const status = response.status;
  const data = await response.json();
  if (status === 200) {
    const indicator = document.getElementById("deposit-withdraw-indicator");
    indicator.classList.remove("deposit-indicator");
    indicator.classList.add("withdraw-indicator");
    indicator.textContent = "The amount is withdraw successfully";

    setBalance();
  } else if (status === 404) {
    // insuficcunte amount
    withdraw_err.style.display = "block";
  }
  console.log(data);
};

// WTHDRAW AND DEPOSIT FOR SAVINGS
savingDeposit.onclick = async (e) => {
  e.preventDefault();

  const id = active_account.value;
  const other_saving_form = document.getElementById("other_saving_form");

  const response = await fetch(
    `http://${window.location.host}/savings-api/deposite-to-saving/${id}`,
    {
      method: "PUT",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: new FormData(other_saving_form),
    }
  );

  const data = response.status;
  if (data === 200) {
    setBalance();
    const indicator = document.getElementById(
      "deposit-withdraw-indicator-other"
    );
    indicator.classList.remove("withdraw-indicator");
    indicator.classList.add("deposit-indicator");
    indicator.textContent = "The amount is deposited successfully";
  }
  console.log(data);
};

savingWithdraw.onclick = async (e) => {
  e.preventDefault();

  const id = active_account.value;
  const other_saving_form = document.getElementById("other_saving_form");

  const response = await fetch(
    `http://${window.location.host}/savings-api/withdraw-to-saving/${id}`,
    {
      method: "PUT",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: new FormData(other_saving_form),
    }
  );

  const status = response.status;

  if (status === 200) {
    setBalance();
    const indicator = document.getElementById(
      "deposit-withdraw-indicator-other"
    );
    indicator.classList.remove("deposit-indicator");
    indicator.classList.add("withdraw-indicator");
    indicator.textContent = "The amount is withdraw successfully";
  } else if (status === 404) {
    withdraw_err.style.display = "block";
  }
};

const splitNumber = document.getElementById("split-number");

splitNumber.onclick = async () => {
  let number = document.getElementById("main-input").value;
  let id = document.getElementById("member-id").value;

  saving_input.value = "";
  compulosry_input.value = "";

  const response = await fetch(
    `http://${window.location.host}/members-api/get-member-detail/${id}`
  );
  const member = await response.json();

  const remain = (member.save_count + 1) * 500;

  // BUTTONS FOR COMPULSORY
  const compulsory_deposit_btn = document.getElementById(
    "compulsory-account-deposit"
  );

  // BUTTONS FOR OTHER
  const saving_deposit_btn = document.getElementById("saving-account-deposit");

  if (member.has_saved) {
    console.log("insert on other saving");
    saving_input.value = number;

    saving_deposit_btn.style.display = "block";
    compulsory_deposit_btn.style.display = "none";
  } else {
    if (number == remain) {
      console.log("insert on compulsory saving");
      compulosry_input.value = number;

      compulsory_deposit_btn.style.display = "block";
      saving_deposit_btn.style.display = "none";
    }

    if (number < 500) {
      console.log("insert on other saving: ", number);

      saving_input.value = number;

      saving_deposit_btn.style.display = "block";
      compulsory_deposit_btn.style.display = "none";
    } else if (number >= 500) {
      if (number % 500 == 0) {
        if (remain > number) {
          console.log("compulsory: ", number);
          compulosry_input.value = number;

          compulsory_deposit_btn.style.display = "block";
          saving_deposit_btn.style.display = "none";
        } else if (number > remain) {
          let other = number - remain;

          compulosry_input.value = remain;
          saving_input.value = other;

          saving_deposit_btn.style.display = "block";
          compulsory_deposit_btn.style.display = "block";

          console.log("other: ", other);
          console.log("compulsory: ", remain);
        } else if (number == remain) {
          console.log("insert on compulsory saving");
        }
      } else {
        if (remain > number) {
          let other = number % 500;
          let compulsory = number - other;

          saving_input.value = other;
          compulosry_input.value = compulsory;

          saving_deposit_btn.style.display = "block";
          compulsory_deposit_btn.style.display = "block";

          console.log("other: ", other);
          console.log("compulsory: ", compulsory);
        } else if (number > remain) {
          let other = number - remain;

          saving_input.value = other;
          compulosry_input.value = remain;

          saving_deposit_btn.style.display = "block";
          compulsory_deposit_btn.style.display = "block";

          console.log("other: ", other);
          console.log("compulsory: ", remain);
        } else if (number === remain) {
          console.log("insert on compulsory saving");
        }
      }
    }
  }
};
