import winreg
import asyncio

import aiohttp
import winsdk.windows.devices.geolocation as wdg

regedit_return = r'SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location'

registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regedit_return, 0, winreg.KEY_ALL_ACCESS)

winreg.SetValueEx(registry_key, 'Value', 0, winreg.REG_SZ, 'Allow')
winreg.CloseKey(registry_key)


async def location() -> dict[str, str]:
    geo_locator = wdg.Geolocator()
    geo_position = await geo_locator.get_geoposition_async()
    geo_latitude = geo_position.coordinate.latitude
    geo_longitude = geo_position.coordinate.longitude

    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(
                f'https://nominatim.openstreetmap.org/reverse?lat={geo_latitude}&lon={geo_longitude}&format=json'
        ) as response:
            response_json = await response.json()
            address = response_json['address']

    return {
        'address': address,
        'latitude': geo_latitude,
        'longitude': geo_longitude
    }


print(asyncio.run(location()))
