# Receive data from the sender and write it to a file
import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8090))

print("[*] Listening for images")


def receive_images():
    while True:
        try:
            data = s.recv(4096)  # Adjust the buffer size as needed
            if not data:
                break
            else:
                print(f"[*] Received {len(data)} bytes")
                # Save the file
                # Make the directory if it doesn't exist
                # directory should be data/<client_name>/images/<filename>
                directory = f"data/{s.getpeername()[0]}/images/"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                filename = "screenshot.png"
                filepath = os.path.join(directory, filename)

                with open(filepath, "ab") as f:
                    f.write(data)
        except Exception as e:
            print(f"Error receiving image: {str(e)}")
            break


if __name__ == "__main__":
    if ()

    receive_images()
