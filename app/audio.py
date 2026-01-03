import alsaaudio
import subprocess
import json
#init alsa
m = alsaaudio.Mixer()


def get_sys_volume() -> int:
    system_volume_arr = m.getvolume()
    system_volume = 0

    for single_volume in system_volume_arr:
        system_volume += single_volume

    system_volume = system_volume / 2 
    system_volume = int(system_volume)

    return system_volume

global_volume = get_sys_volume()


def update_global_volume(volume: int):
    global_volume = volume

def get_global_volume() -> int:
    return global_volume


def get_sys_outputs() -> list[list[int | str]]:

    result = subprocess.run(
        ["pactl", "-f", "json", "list", "sinks"],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    data = json.loads(result)

    outputs_arr = []

    for device in data:
        device_data = [
            device["index"],
            device["description"],
        ]

        outputs_arr.append(device_data)

    return outputs_arr


def set_sys_output(device_id: int):
    subprocess.run(
        ["pactl", "set-default-sink", str(device_id)],
        check=True
    )


def set_sys_volume(chanel: int , volume: int):
    m.setvolume(volume , chanel)
    
    if chanel == 0:
        update_global_volume(volume)

def get_current_output() -> list[int | str]:
    default_name = subprocess.run(
        ["pactl", "get-default-sink"],
        capture_output=True,
        text=True,
        check=True
    ).stdout.strip()

    sinks_json = subprocess.run(
        ["pactl", "--format=json", "list", "sinks"],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    sinks = json.loads(sinks_json)

    sink_id = None
    description = None

    for sink in sinks:
        if sink["name"] == default_name:
            sink_id = sink["index"]
            description = sink["description"]
            break

    data = [
        sink_id,
        description
    ]

    return data



