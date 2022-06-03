import joy_auth as auth

login = input("Enter LOGIN: ")
passwd = input("Enter PASSWORD: ")
result = auth.syncAuthorize(login, passwd)

if result[0] == None:
    print("Problems with authorization. Please try again!")
    print(f"Status {result[1]}")
else:
    print(result[0]) 