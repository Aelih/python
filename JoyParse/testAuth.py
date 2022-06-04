import joy_auth as auth
import asyncio

async def AuthTry(login, passwd):
    #result = auth.syncAuthorize(login, passwd)

    Tasks = []
    Tasks.append(asyncio.create_task(auth.asyncAuthorize(login, passwd)))

    result = await asyncio.gather(*Tasks)

    if result[0][0] == None:
        print("Problems with authorization. Please try again!")
        print(f"Status {result[0][1]}")
    else:
        print(result[0][0]) 


if __name__ == "__main__":
    login = input("Enter LOGIN: ")
    passwd = input("Enter PASSWORD: ")
    asyncio.run(AuthTry(login, passwd))