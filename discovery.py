from monitor import get_supported_monitor_inputs
import topics

LIGHT_DISCOVERY = {
    "name": "Display",
    "icon": "mdi:monitor",
    "command_topic": topics.BRIGHTNESS_COMMAND_TOPIC,
    "state_topic": topics.BRIGHTNESS_STATE_TOPIC,
    "brightness_command_topic": topics.BRIGHTNESS_COMMAND_TOPIC,
    "brightness_state_topic": topics.BRIGHTNESS_STATE_TOPIC,
    "brightness_scale": 100,
    "effect_command_topic": topics.EFFECTS_COMMAND_TOPIC,
    "effect_state_topic": topics.EFFECTS_STATE_TOPIC,
    "effect_list": list(get_supported_monitor_inputs().values()),
    "unique_id": "monitor_display",
    "device": {
        "identifiers": ["monitor_display"],
        "name": "Monitor",
        "model": "Generic Monitor",
        "manufacturer": "Generic"
    }
}