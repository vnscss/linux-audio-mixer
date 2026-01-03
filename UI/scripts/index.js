

async function get_master_volume(){
    let volume = await window.pywebview.api.get_global_volume();
    return volume;
}

async function draw_master_volume(){
    let range_input = document.querySelector("#master_volume");
    range_input.value = await get_master_volume();
}

async function update_master_volume(volume) {
   await window.pywebview.api.set_sys_volume(parseInt(volume));
   return;
}

async function load_outputs() {
    let output_devices = await window.pywebview.api.get_sys_outputs()
    let select = document.querySelector("#master_devices");
    
    select.innerHTML = '';

    output_devices.forEach(device => {
        let option = document.createElement('option');

        option.value = device[0];
        option.text = device[1];

        select.appendChild(option);
    });

    let current_output = await window.pywebview.api.get_current_output()

    select.value = current_output[0]

}


async function set_sys_output(device) {
    await window.pywebview.api.set_sys_output(device)
    return;
}

async function master_mute_button_change() {
    let masterCheckbox = document.querySelector('#master_mute');

    if (masterCheckbox.checked) {
        await window.pywebview.api.master_unmute()
    } else {
        await window.pywebview.api.master_mute()
    }
}

function front_end_check_mute(){
    let masterCheckbox = document.querySelector('#master_mute');
    masterCheckbox.checked = true;
    console.log(1)
}

window.addEventListener("pywebviewready", async () => {
    draw_master_volume()
    load_outputs()

    let range = document.querySelector("#master_volume");
    range.addEventListener("input", (e) => {
        update_master_volume(e.target.value);
        front_end_check_mute();
    });


    let master_output = document.querySelector("#master_devices");
    master_output.addEventListener("input", (e) => {
        set_sys_output(e.target.value);
    });


    let masterCheckbox = document.querySelector('#master_mute');
    masterCheckbox.addEventListener('change', async () => {
        master_mute_button_change() 
    });

});