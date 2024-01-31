from inputs import get_gamepad
from threading import Thread

get_binary = lambda x, n: format(x, 'b').zfill(n)

class XboxController:
  def __init__(self):
    # Joysticks
    self.joystick_left_x = 0    # 2 bytes (signed)
    self.joystick_left_y = 0    # 2 bytes (signed)
    self.joystick_right_x = 0   # 2 bytes (signed)
    self.joystick_right_y = 0   # 2 bytes (signed)

    # Triggers and bumpers
    self.trigger_left = 0       # 1 byte (unsigned)
    self.trigger_right = 0      # 1 byte (unsigned)
    self.bumper_left = 0        # 1 bit
    self.bumper_right = 0       # 1 bit

    # Dpad
    self.dpad_up = 0            # 1 bit
    self.dpad_right = 0         # 1 bit
    self.dpad_down = 0          # 1 bit
    self.dpad_left = 0          # 1 bit

    # Face buttons
    self.button_north = 0       # 1 bit
    self.button_east = 0        # 1 bit
    self.button_south = 0       # 1 bit
    self.button_west = 0        # 1 bit

    # Extra buttons
    self.button_select = 0      # 1 bit
    self.button_start = 0       # 1 bit
    self.button_thumb_left = 0  # 1 bit
    self.button_thumb_right = 0 # 1 bit
  
  def get_state(self):
    # Create a 94 + 2 bit state
    state_string = ''

    # Joysticks
    joystick_state = ''
    # Convert signed joystick states to unsigned values
    joystick_state += get_binary(self.joystick_left_x + 2**15, 16)
    joystick_state += get_binary(self.joystick_left_y + 2**15, 16)
    joystick_state += get_binary(self.joystick_right_x + 2**15, 16)
    joystick_state += get_binary(self.joystick_right_y + 2**15, 16)
    
    # Triggers and bumpers
    trigger_state = ''
    trigger_state += get_binary(self.trigger_left, 8)
    trigger_state += get_binary(self.trigger_right, 8)
    trigger_state += get_binary(self.bumper_left, 1)
    trigger_state += get_binary(self.bumper_right, 1)

    # Dpad and buttons
    buttons_state = ''
    buttons_state += get_binary(self.dpad_up, 1)
    buttons_state += get_binary(self.dpad_right, 1)
    buttons_state += get_binary(self.dpad_down, 1)
    buttons_state += get_binary(self.dpad_left, 1)
    buttons_state += get_binary(self.button_north, 1)
    buttons_state += get_binary(self.button_east, 1)
    buttons_state += get_binary(self.button_south, 1)
    buttons_state += get_binary(self.button_west, 1)
    
    # Extra buttons
    extra_state = ''
    extra_state += get_binary(self.button_select, 1)
    extra_state += get_binary(self.button_start, 1)
    extra_state += get_binary(self.button_thumb_left, 1)
    extra_state += get_binary(self.button_thumb_right, 1)

    # Concat everything
    state_string += joystick_state
    state_string += trigger_state
    state_string += buttons_state
    state_string += extra_state

    # Add 2 bit padding
    state_string += "00"

    # Convert to bytes
    return int(state_string, 2).to_bytes(12)
    
  def update(self):
    for event in get_gamepad():
      code, state = event.code, event.state

      match code:
        # Joystick controls
        case "ABS_X":
          self.joystick_left_x = state
        case "ABS_Y":
          self.joystick_left_y = state
        case "ABS_RX":
          self.joystick_right_x = state
        case "ABS_RY":
          self.joystick_right_y = state
        
        # Trigger and bumper controls
        case "ABS_Z":
          self.trigger_left = state
        case "ABS_RZ":
          self.trigger_right = state
        case "BTN_TL":
          self.bumper_left = state
        case "BTN_TR":
          self.bumper_right = state
        
        # Left and right arrows
        case "ABS_HAT0X":
          if state == 1:
            self.dpad_left = 0
            self.dpad_right = 1
          elif state == -1:
            self.dpad_left = 1
            self.dpad_right = 0
          else:
            self.dpad_left = 0
            self.dpad_right = 0

        # Up and down arrows
        case "ABS_HAT0Y":
          if state == 1:
            self.dpad_up = 0
            self.dpad_down = 1
          elif state == -1:
            self.dpad_up = 1
            self.dpad_down = 0
          else:
            self.dpad_up = 0
            self.dpad_down = 0

        # Y, B, A, X buttons
        case "BTN_NORTH":
          self.button_north = state
        case "BTN_EAST":
          self.button_east = state
        case "BTN_SOUTH":
          self.button_south = state
        case "BTN_WEST":
          self.button_west = state

        case "BTN_START":
          self.button_start = state
        case "BTN_SELECT":
          self.button_select = state

        # Joystick pressed down
        case "BTN_THUMBL":
          self.button_thumb_left = state
        case "BTN_THUMBR":
          self.button_thumb_right = state

        # Sync message
        case "SYN_REPORT":
          pass

        case _:
          raise NotImplementedError(f"Event {code} is not implemented.")

  def _main_loop(self):
    while True:
      self.update()

  def run(self):
    # Create controller thread
    controller_thread = Thread(target=self._main_loop, daemon=True)
    controller_thread.start()

def main():
  controller = XboxController()
  controller.run()
  while True:
    print(controller.get_state())
    
if __name__ == "__main__":
  main()
