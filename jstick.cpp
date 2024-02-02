#include <linux/joystick.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

int main() {
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