#include <cstdint>
#include <iostream>
#include <zmq.hpp>

// Define the structure to match the 12-byte data layout
struct XboxControllerState {
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

int main() {
  zmq::context_t context(1);
  zmq::socket_t socket(context, ZMQ_SUB);

  // Connect to the publisher socket
  socket.connect("tcp://127.0.0.1:5556");
  socket.set(zmq::sockopt::subscribe, "");

  std::cout << "Listening on port 5556 ..." << std::endl;

  while (true) {
    zmq::message_t message;
    socket.recv(message, zmq::recv_flags::none);

    std::cout << "Received message of size " << message.size() << " bytes" << std::endl;

    if (message.size() == sizeof(XboxControllerState)) {
      XboxControllerState state;
      memcpy(&state, message.data(), sizeof(XboxControllerState));

      std::cout << "Joystick Left X: " << state.joystick_left_x << ", Y: " << state.joystick_left_y << std::endl;
      std::cout << "Joystick Right X: " << state.joystick_right_x << ", Y: " << state.joystick_right_y << std::endl;
      std::cout << "Trigger Left: " << static_cast<int>(state.trigger_left)
                << ", Trigger Right: " << static_cast<int>(state.trigger_right) << std::endl;
      std::cout << "DPad & Buttons: " << std::hex << static_cast<int>(state.dpad_and_buttons) << std::dec << std::endl;
    }
  }

  return 0;
}