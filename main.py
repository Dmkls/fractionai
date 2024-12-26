import asyncio
import aiohttp
import fake_useragent
from colorama import Fore
from random import randint

THREATS = 10
THREATS_DELAY = (1, 30) # delay in seconds before account processing starts
URL: str = "https://backend.fractionai.xyz/api/waitList/createWaitlist"
with open("emails.txt", 'r+') as f:
    emails = list(filter(bool, f.read().splitlines()))  # file to list
emails_total = len(emails)

print(Fore.RED + f"Creating user agents, please wait")
user_agents = [fake_useragent.UserAgent().random for _ in range(emails_total)]
print(Fore.GREEN + f"User agents were successfully created")

def hello_message():
    print(Fore.GREEN + f"Found {emails_total} email/s to process\n"
                       f"Starting..\n")


def create_tasks():
    semaphore = asyncio.Semaphore(THREATS)
    tasks = [process_emails(email, ua, semaphore) for email, ua in zip(emails, user_agents)]
    return tasks


async def add_email_to_waitlist(email: str, header: dict) -> bool:
    await asyncio.sleep(randint(THREATS_DELAY[0], THREATS_DELAY[1]))
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json={'email': email}, headers=header) as response:
            if response.status == 201:
                print(Fore.GREEN + f"{email} - was registered successfully!")
                return True
            else:
                print(Fore.RED + f"{email} - error occurred while sending a request.")
                return False


async def process_emails(email: str, ua: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        if not await add_email_to_waitlist(email, {'User-Agent': ua,}):
            with open('failed_emails.txt', 'a') as failed:
                failed.write(f"{email}\n")


async def main():
    hello_message()
    await asyncio.gather(*create_tasks())


if __name__ == "__main__":
    asyncio.run(main())
