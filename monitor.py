import re
import subprocess

# TODO: add support for volume control
# TODO: add support for temperature control

def set_monitor_brightness(brightness):
    try:
        subprocess.run(["ddcutil", "setvcp", "10",
                       str(brightness)], check=True)
        print(f"Monitor brightness set to {brightness}%")
    except subprocess.CalledProcessError as e:
        print(f"Error setting brightness: {e}")


def get_monitor_brightness(log=True):
    try:
        result = subprocess.run(["ddcutil", "getvcp", "10"],
                                capture_output=True, text=True, check=True)
        brightness = int(result.stdout.split(
            "current value =")[1].split(",")[0].strip())
        if log:
            print(f"Current monitor brightness: {brightness}%")
        return brightness
    except subprocess.CalledProcessError as e:
        print(f"Error getting brightness: {e}")
        return None


def toggle_monitor_power_state(power):
    try:
        if power:
            subprocess.run(["ddcutil", "setvcp", "D6", "0x01"], check=True)
            print("Monitor powered ON")
        else:
            subprocess.run(["ddcutil", "setvcp", "D6", "0x04"], check=True)
            print("Monitor powered OFF")
    except subprocess.CalledProcessError as e:
        print(f"Error setting power state: {e}")


def get_monitor_power_state(log=True):
    try:
        result = subprocess.run(["ddcutil", "getvcp", "D6"],
                                capture_output=True, text=True, check=True)
        output = result.stdout
        match = re.search(r"sl=0x([0-9a-fA-F]+)", output)
        if match:
            power_state = match.group(1).strip()
            if log:
                print(f"Current monitor power state: 0x{power_state}")
            return f"0x{power_state}"
        else:
            print("Power state not found in the output.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting power state: {e}")
        return None


def set_monitor_input(input_name):
    try:
        supported_monitor_inputs = get_supported_monitor_inputs(False)
        input_id = None
        for key, value in supported_monitor_inputs.items():
            if value == input_name:
                input_id = key
                break
        if input_id is not None:
            subprocess.run(["ddcutil", "setvcp", "60",
                           str(input_id)], check=True)
            print(f'Monitor input set to {input_name} (id: {input_id})')
        else:
            print(f"Input name '{input_name}' not found in supported inputs.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting input: {e}")


def get_current_monitor_input(log=True):
    try:
        result = subprocess.run(["ddcutil", "getvcp", "60"],
                                capture_output=True, text=True, check=True)
        output = result.stdout
        match = re.search(r"sl=0x([0-9a-fA-F]+)", output)
        if match:
            input_id = '0x%s' % match.group(1).strip()
            input_name = get_supported_monitor_inputs(False)[input_id]
            if log:
                print('Current monitor input: %s' % input_name)
            return input_name
        else:
            print("Input ID not found in the output.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting input: {e}")
        return None


def get_supported_monitor_inputs(verbose=True):
    try:
        result = subprocess.run(["ddcutil", "capabilities"],
                                capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        output = result.stdout
        match = re.search(
            r"Feature: 60 \(Input Source\)(.*?)Feature:", output, re.DOTALL)
        if match:
            inputs_section = match.group(1)
            inputs = re.findall(r"\s*([0-9a-fA-F]+):\s*(.*)", inputs_section)
            inputs_dict = {'0x%s' % input_id: input_name.strip()
                           for input_id, input_name in inputs}
            if verbose:
                print(f"Available monitor inputs: {inputs_dict}")
            return inputs_dict
        else:
            print("Input sources not found in the output.")
            return None
    except (subprocess.CalledProcessError, IndexError, UnicodeDecodeError) as e:
        print(f"Error getting monitor inputs: {e}")
        return None
