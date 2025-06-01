import asyncio
from vitap_vtop_client.client import VtopClient
from vitap_vtop_client.exceptions import VitapVtopClientError, VtopLoginError

async def main():
    async with VtopClient("24MIC7076", "%_9pJfQVcc$E!fh") as client:
        try:
            fall_sem_2024_25 = "AP2024253"
            attendance_data = await client.get_attendance(sem_sub_id=fall_sem_2024_25)
            print(attendance_data)

        except VtopLoginError as e:
            print(f"A login-specific error occurred: {e}")
        except VitapVtopClientError as e:
            print(f"A client error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
