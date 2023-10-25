import socket

def main():
    server_host = 'localhost'  # Change to the server's hostname or IP address
    server_port = 6789

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(5)  # Set a timeout for the server reply (5 seconds)
            
            # Get user input for N and the list of N numbers
            N = int(input("Enter the number of elements (N): "))
            numbers = input("Enter the list of numbers separated by spaces: ")
            numbers_list = [int(x) for x in numbers.split()]

            # Send N and the list of numbers to the server
            message = f"{N} {' '.join(map(str, numbers_list))}"
            sock.sendto(message.encode(), (server_host, server_port))

            # Receive and print the sorted list from the server
            data, _ = sock.recvfrom(1000)
            sorted_numbers = data.decode().split()
            print("Sorted List:", ' '.join(sorted_numbers))

    except socket.error as e:
        print(f"Socket error: {e}")
    except socket.timeout:
        print("Server did not reply within the timeout.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
