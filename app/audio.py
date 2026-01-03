import alsaaudio
import subprocess
import json

class AudioAPI:
    def __init__(self):
        self.m = alsaaudio.Mixer()
        self.global_volume = self.get_sys_volume()



    def get_sys_volume(self) -> int:
        system_volume_arr = self.m.getvolume()
        system_volume = 0

        for single_volume in system_volume_arr:
            system_volume += single_volume

        system_volume = system_volume / 2 
        system_volume = int(system_volume)

        return system_volume


    def update_global_volume(self, volume: int):
        self.global_volume = volume

    def get_global_volume(self) -> int:
        return self.global_volume


    def get_sys_outputs(self) -> list[list[int | str]]:

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


    def set_sys_output(self, device_id: int):
        subprocess.run(
            ["pactl", "set-default-sink", str(device_id)],
            check=True
        )

        volume = self.get_global_volume()
        self.set_sys_volume(volume)
        


    def set_sys_volume(self , volume: int):
        self.m.setvolume(volume , 0)
        self.m.setvolume(volume , 1)
        self.update_global_volume(volume)

    def set_sys_single_chanel_volume(self ,chanel: int , volume: int):
        self.m.setvolume(volume , chanel)
        
        if chanel == 0:
            self.update_global_volume(volume)

    def get_current_output(self) -> list[int | str]:
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

    def master_mute(self):
        volume = 0
        self.m.setvolume(volume , 0)
        self.m.setvolume(volume , 1)

    def master_unmute(self):
        volume = self.get_global_volume()
        self.m.setvolume(volume , 0)
        self.m.setvolume(volume , 1)