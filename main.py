import asyncio
import aiohttp
import fake_useragent
import aiofiles
from colorama import Fore, Style

URL: str = "https://backend.fractionai.xyz/api/waitList/createWaitlist"

async def read_emails():
    tasks = []  
    async with aiofiles.open("emails.txt", mode='r') as f:
        async for line in f:
            email = line.split(":")[0].strip()
            ua = fake_useragent.UserAgent().random
            header = {'User-Agent': ua}
            tasks.append(add_email_to_waitlist(email, header))

    await asyncio.gather(*tasks)

async def add_email_to_waitlist(email: str, header: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json={'email': email}, headers=header) as response:
            if response.status == 201:
                print(Fore.GREEN + f"{email} - was registered successfully!")
            else:
                print(Fore.RED + f"{email} - error occurred while sending a request.")

async def main():
    await read_emails()

if __name__ == "__main__":
    asyncio.run(main())
