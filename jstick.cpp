#include <linux/joystick.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <thread>
#include <chrono>

struct ControllerState {
  // Joysticks (4 x 2 bytes = 8 bytes)
  int16_t joystick_left_x;
  int16_t joystick_left_y;
  int16_t joystick_right_x;
  int16_t joystick_right_y;

  // Triggers (2 x 1 byte = 2 bytes)
  uint8_t trigger_left;
  uint8_t trigger_right;

  // Buttons and D-pad (1 byte + 1 byte for padding and extra buttons = 2 bytes)
  uint8_t dpad_and_buttons; // This will contain dpad, face buttons, and extra buttons
  uint8_t padding; // Padding to align to 12 bytes, includes unused bits and thumb buttons
};

struct controller_task {
  ControllerState& cstate;

  controller_task(ControllerState& state):cstate(state) {}

  int operator() () {
    // Connect to joystick
    const char* device = "/dev/input/js1";
    int js = open(device, O_RDONLY);
    if (js < 0) {
      std::cerr << "Could not open joystick device." << std::endl;
      return -1;
    }

    struct js_event event;
    while (read(js, &event, sizeof(event)) > 0) {
      switch (event.type) {
        case JS_EVENT_BUTTON:
          std::cout << "Button " << (int)event.number
                    << " is " << (event.value ? "pressed" : "released") << std::endl;
          break;
        case JS_EVENT_AXIS:
          std::cout << "Axis " << (int)event.number
                    << " is at position " << event.value << std::endl;
          break;
        default:
          // Ignore other events
          break;
      } 
    }

    close(js);
    return 0;
  }
};

int main() {
  ControllerState state;
  controller_task task(state);

  std::thread controller_thread(task);
  
  while (true) {
    std::cout << "Ping" << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
  }

  return 0;
}