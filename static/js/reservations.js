function popup(element) {
    let type = element.dataset.type;
    document.querySelector("#cancel_ticket_btn").dataset.type = type;
    document.querySelector(".popup").style.display = 'block';
}

function remove_popup() {
    document.querySelector(".popup").style.display = 'none';
    document.querySelector("#cancel_ticket_btn").dataset.type = "";
}

function cancel_tkt() {
    let type = document.querySelector("#cancel_ticket_btn").dataset.type;
    let formData = new FormData();
    formData.append('type',type)
    fetch('reservation/cancel',{
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(response => {
        if (response.success === true) {
            remove_popup();
            document.querySelector(`[id='${type}'] .ticket-action-div`).innerHTML = '';
            document.querySelector(`[id='${type}'] .status-div`).innerHTML = `<div class="red">CANCELLED</div>`;
            document.querySelector(`[id='${type}'] .booking-date-div`).innerHTML = '';
        }
        else {
            remove_popup();
            alert(`Error: ${response.error}`)
        }
    });
}