import zmq

from xkontrol import XboxController

def setup_zmq_socket(port="5556"):
  # Create zmq session
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  socket.bind(f"tcp://*:{port}")
  return socket

def main():
  socket = setup_zmq_socket()

  controller = XboxController()
  controller.run()

  while True:
    current_state = controller.get_state()

    # Convert the bytes to a binary string
    binary_state_str = ' '.join(f'{byte:08b}' for byte in current_state)
    print(binary_state_str)
    
    # Send the raw bytes state over zmq
    socket.send(current_state)

if __name__ == "__main__":
  main()
