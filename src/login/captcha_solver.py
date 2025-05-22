import base64
import io
import json
import numpy as np
from PIL import Image
import httpx
import importlib.resources
import asyncio

from src.constants import VTOP_LOGIN_URL, HEADERS
from src.utils import find_captcha

MAX_RETRIES_FETCH = 3 # Max retries for *fetching* the captcha image

# Loading the ML Model using importlib.resources
weights = None
biases = None
try:
    # Use read_text or open_text to access data files within the package
    weights_data_str = importlib.resources.read_text('src.resources', 'weights.json')
    model_config = json.loads(weights_data_str)
    weights = np.array(model_config.get("weights"))
    biases = np.array(model_config.get("biases"))
    if weights is not None and biases is not None:
        print("Captcha weights loaded successfully.")
    else:
        print("Warning: 'weights' or 'biases' key missing in weights.json")
        weights = None 
        biases = None
except FileNotFoundError:
    print("Error: weights.json not found in package data.")
except json.JSONDecodeError:
    print("Error: weights.json is not valid JSON.")
except Exception as e:
    print(f"Error loading captcha weights.json: {e}")
    weights = None
    biases = None
    print("Captcha solving disabled due to load error.")


async def fetch_captcha(client: httpx.AsyncClient, retries=MAX_RETRIES_FETCH) -> str | None:
    """
    Fetches the VTOP login page and extracts the base64 encoded captcha image.

    Args:
        client (httpx.AsyncClient): Client object for making HTTP requests.
        retries (int): Number of retries for fetching captcha.

    Returns:
        str or None: Base64 encoded captcha image data (excluding the data URI prefix)
                     if found, otherwise None.

    Raises:
        httpx.RequestError: If the HTTP request fails after all retries.
        ValueError: If captcha image is not found in the response after all retries.
    """
    for attempt in range(retries):
        print(f"Fetching captcha, attempt {attempt + 1}/{retries}...")
        try:
            # Use await client.get
            response = await client.get(VTOP_LOGIN_URL, headers=HEADERS)
            response.raise_for_status() # Raise exception for bad status codes

            base64_code = find_captcha.find_captcha(response.text)

            if base64_code: # Check if utility returned a value (not None)
                print("Captcha base64 found.")
                return base64_code
            else:
                print("Captcha base64 not found in response.")
                if attempt < retries - 1:
                    print("Retrying captcha fetch...")
                    await asyncio.sleep(1) # Small delay before retry
                else:
                    raise ValueError(f"Captcha image not found in response after {retries} attempts.")

        except httpx.RequestError as e:
            print(f"Failed to fetch captcha page: {e}")
            if attempt < retries - 1:
                 print("Retrying captcha fetch...")
                 await asyncio.sleep(1)
            else:
                raise httpx.RequestError(f"Failed to fetch captcha page after {retries} attempts: {e}") from e
        except ValueError as e:
            # Re-raise ValueError if captcha not found
            raise e # Captcha not found after all attempts
        except Exception as e:
            print(f"An unexpected error occurred during captcha fetch attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                 print("Retrying captcha fetch...")
                 await asyncio.sleep(1)
            else:
                raise Exception(f"An unexpected error occurred during captcha fetch after {retries} attempts: {e}") from e

    # Should not be reached if exceptions are raised correctly
    return None

# Synchronous function as it's CPU-bound
def partition_img(img: np.ndarray) -> list[np.ndarray]:
    """Partitions the captcha image into 6 character images."""
    parts = []
    try:
        for i in range(6):
            x1 = (i + 1) * 25 + 2
            y1 = 7 + 5 * (i % 2) + 1
            x2 = (i + 2) * 25 + 1
            y2 = 35 - 5 * ((i + 1) % 2)
            # select the bounding box 
            part = img[y1:y2, x1:x2]
            parts.append(part)
        return parts
    except Exception as e:
        print(f"Error during captcha image partitioning: {e}")
        raise ValueError(f"Failed to partition captcha image: {e}") from e


# Synchronous function as it's CPU-bound
def convert_to_abs_bw(img: np.ndarray) -> np.ndarray:
    """Converts an image part to absolute black and white based on average pixel value."""
    if img.size == 0:
        raise ValueError("Cannot process empty image part.")
    avg = np.sum(img)
    avg /= 24 * 22
    return np.where(img > avg, 0, 1)

def _solve_captcha_ml(img: list[np.ndarray]) -> str | None:
    LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    captcha = ""
    for single_letter in img:
        dw_img = convert_to_abs_bw(single_letter)
        dw_img = dw_img.flatten()
        x = np.dot(dw_img, weights) + biases
        x = np.exp(x)
        captcha += LETTERS[np.argmax(x)]
    if len(captcha) != 6:
        print(f"Warning: Captcha solving resulted in unexpected output: {captcha}")
        # Decide if this counts as a total failure. For now, return None.
        return None
    return captcha

# Synchronous function as it's CPU-bound
def solve_captcha(captcha_base64: str) -> str | None:
    """
    Solves the given base64 encoded captcha image using the loaded ML model.

    Args:
        captcha_base64 (str): Base64 encoded captcha image data (excluding prefix).

    Returns:
        str or None: The predicted captcha text, or None if solving fails
                     or model is not loaded.
    """
    if weights is None or biases is None:
        print("Captcha solving model not loaded.")
        return None

    try:
        img = _str_to_img(captcha_base64)
        # Optional: Apply convert_to_abs_bw here
        # img = convert_to_abs_bw(img)
        parts = partition_img(img)
        return _solve_captcha_ml(parts)

    except ValueError as e:
        print(f"Captcha solving failed due to image processing error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during captcha solving: {e}")
        return None

# Synchronous function as it's CPU-bound
def _str_to_img(src: str) -> np.ndarray:
    """Decodes base64 string to a grayscale NumPy array."""
    try:
        im = base64.b64decode(src)
        img = Image.open(io.BytesIO(im)).convert("L") # Convert to grayscale
        img = np.array(img)
        return img
    except Exception as e:
        print(f"Error decoding base64 to image: {e}")
        raise ValueError(f"Failed to decode base64 to image: {e}") from e