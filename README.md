# vitap-vtop-client - Python Client for VIT-AP VTOP Portal

`vitap-vtop-client` is a Python library that provides a programmatic interface for interacting with the VIT-AP VTOP student portal. It abstracts away the complexities of web scraping, session management, CAPTCHA handling, and parsing HTML responses, offering structured data access to various student information sections.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Endpoints](#endpoints)
5. [Example Usage](#example-usage)
6. [Contributing](#contributing)
7. [License](#license)
8. [Future Updates](#future-updates)
9. [Companion App](#companion-app)

## Overview
`vitap-vtop-client` is a Python library that provides a programmatic interface for interacting with the VIT-AP VTOP student portal. It abstracts away the complexities of web scraping, session management, CAPTCHA handling, and parsing HTML responses, offering structured data access to various student information sections.

This library is designed to serve as a backend component for applications that need to retrieve data from the VTOP portal, such as mobile apps, web services, or analytical tools.

**Disclaimer:** Use this library responsibly and in accordance with VIT-AP's terms of service. Web scraping is subject to changes in the target website's structure, which may occasionally affect the library's functionality.

## Features
-   User authentication and session management.
-   Retrieving student profile information.
-   Accessing academic details like attendance, timetable, marks, and exam schedules.
-   Fetching biometric log entries.
-   Viewing mentor, HOD, and Dean details.
-   Checking financial information, including pending payments and receipts.
-   Posting and reviewing hostel outing requests (weekend and general).
-   Retrieving NCGPA and rank details.

## Installation
To use the API, clone the repository and install the required dependencies.

```bash
git clone https://github.com/Udhay-Adithya/vitap-vtop-client.git

cd vitap-vtop-client

pip install -r requirements.txt
```

For a detailed setup information see [CONTRIBUTING.md](/CONTRIBUTING.md)


## Endpoints

Refer to the main documentation [`DOCS.md`](/DOCS.md) for all available usage options.

## Example Usage
### Login and Fetch Attendance
```python
async def main():
    async with VtopClient("your_registration_number", "your_password") as client:
        try:
            fall_sem_2024_25 = "AP2024252"
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
```

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](/CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

## Future Updates
We are committed to improving this library. Future updates will include new features, bug fixes, and performance improvements.

## VTOP-API
I have also developed a light-weight FastAPI Wrapper for this library. The VITAP-VTOP API Lets everyone to access and retreive data from VTOP at ease. You can find the app repository [here](https://github.com/Udhay-Adithya/vit_ap_vtop_api/).

We encourage users to try out the API and provide feedback. Future updates will enhance both the library and the API to better serve the needs of VIT-AP students.

