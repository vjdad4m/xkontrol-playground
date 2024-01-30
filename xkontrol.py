from inputs import get_gamepad
from threading import Thread

class ControllerState:
  def __init__(self):
    self.joystick_left_x = 0
    self.joystick_left_y = 0
    self.joystick_right_x = 0
    self.joystick_right_y = 0
    self.trigger_left = 0
    self.button_left = 0
    self.trigger_right = 0
    self.button_right = 0
    self.dpad_left = 0
    self.dpad_right = 0
    self.dpad_up = 0
    self.dpad_down = 0
    self.button_north = 0
    self.button_east = 0
    self.button_south = 0
    self.button_west = 0
    self.button_select = 0
    self.button_start = 0
    self.button_thumb_left = 0
    self.button_thumb_right = 0
  
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
        
        # Trigger controls
        case "ABS_Z":
          self.trigger_left = state
        case "BTN_TL":
          self.button_left = state
        case "ABS_RZ":
          self.trigger_right = state
        case "BTN_TR":
          self.button_right = state
        
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
          raise NotImplementedError(code)

  def _main_loop(self):
    while True:
      self.update()

  def run(self):
    controller_thread = Thread(target=self._main_loop, daemon=True)
    controller_thread.start()

def main():
  controller = ControllerState()
  controller.run()
  while True:
    print(controller.joystick_left_x, controller.joystick_left_y)
    
if __name__ == "__main__":
  main()
