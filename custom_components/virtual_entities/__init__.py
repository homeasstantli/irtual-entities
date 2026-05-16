"""Virtual Entities — Home Assistant integration with Firebase pairing."""
import random
import logging
import aiohttp

DOMAIN = "virtual_entities"
_LOGGER = logging.getLogger(__name__)

FIREBASE_DATABASE_URL = "https://virtual-entities-default-rtdb.firebaseio.com"
FIREBASE_SECRET       = "ObYZguJeZxsn6Vub6B7FRlC4YEA2O1NWIMvDkmn1"
HA_EXTERNAL_URL       = "http://192.168.1.206:8123"
HA_LONG_LIVED_TOKEN   = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZGM1MzE0YjI1NDg0Y2ZhOGY5MmZlZjkyMzI4YTYzYiIsImlhdCI6MTc3ODg5NzE0OCwiZXhwIjoyMDk0MjU3MTQ4fQ.-pgf10Kdhb0HpfgSTdXO8zY6PL21d1iAopqsNakuwOw"

def _generate_code(length=6):
    return "".join(random.choices(string.digits, k=length))

async def async_setup(hass, config):
    code = _generate_code()
    payload = {
        "used": False,
        "ha_url": HA_EXTERNAL_URL,
        "ha_token": HA_LONG_LIVED_TOKEN,
    }
    url = f"{FIREBASE_DATABASE_URL}/pairing/{code}.json?auth={FIREBASE_SECRET}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=payload) as resp:
                if resp.status == 200:
                    _LOGGER.info("Pairing code written: %s", code)
                else:
                    _LOGGER.error("Firebase write failed: %s", resp.status)
    except Exception as e:
        _LOGGER.error("Could not reach Firebase: %s", e)

    hass.components.persistent_notification.async_create(
        title="🔗 Virtual Entities — Pairing Code",
        message=(
            f"## Your one-time pairing code:\n\n"
            f"# **{code}**\n\n"
            f"Enter this in the Virtual Entities web app to connect.\n"
            f"This code expires after one use."
        ),
        notification_id="virtual_entities_pairing",
    )
    return True
