import socket


def main():
    server_port = 6789
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("localhost", server_port))
            print(f"UDP server listening on port {server_port}")

            while True:
                data, client_address = sock.recvfrom(1000)
                message_parts = data.decode().split()

                if len(message_parts) >= 2:
                    N = int(message_parts[0])
                    numbers = [int(x) for x in message_parts[1:]]
                    print(f"Received the following list: {numbers}")
                    sorted_numbers = sorted(numbers)

                    # Send the sorted list back to the client
                    reply_message = " ".join(map(str, sorted_numbers))
                    sock.sendto(reply_message.encode(), client_address)
                    print("Sorted list sent successfully!")

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
