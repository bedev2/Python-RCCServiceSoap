from RCCServiceSoap import RCCServiceSoap

def main():
    try:
        client = RCCServiceSoap("127.0.0.1", 64000, 5)
        
        tests = [
            ("HelloWorld", client.HelloWorld),
            ("GetVersion", client.GetVersion),
            ("GetStatus", client.GetStatus)
        ]

        print("Tests are running:")
        for name, func in tests:
            result = func()
            print(f"{name}: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()