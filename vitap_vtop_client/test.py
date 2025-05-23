import asyncio
from .client import VtopClient
from .exceptions import VitapVtopClientError, VtopLoginError
"""
Sandeepak
23bce7626
Vamshikrishna@191$

Udhay
g4st=sTevi

Tejas
23BCE7754
Suitup@2121
"""

async def main():
    async with VtopClient("23bce7626", "Vamshikrishna@191$") as client:
        try:
            fall_sem_regular = "AP2024256"
            # attendance_data = await client.get_attendance(sem_sub_id=fall_sem_regular)
            # print(attendance_data)

            # biometric_data = await client.get_biometric(date="11/04/2025")
            # print(biometric_data)

            # timetable_data = await client.get_timetable(sem_sub_id=fall_sem_regular)
            # print(timetable_data)

            mentor_data = await client.get_profile()
            print(mentor_data)


        except VtopLoginError as e:
            print(f"A login-specific error occurred: {e}")
        except VitapVtopClientError as e:
            print(f"A client error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())