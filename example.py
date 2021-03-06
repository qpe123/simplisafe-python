"""Run an example script to quickly test any SimpliSafe system."""
import asyncio

from aiohttp import ClientSession

import simplipy
from simplipy.errors import SimplipyError


async def exercise_client(
        email: str, password: str, websession: ClientSession) -> None:
    """Test a SimpliSafe client (regardless of version)."""
    print('{0}'.format(email))
    print('========================')

    systems = await simplipy.get_systems(email, password, websession)
    for idx, system in enumerate(systems):
        print()
        print('System #{0}'.format(idx + 1))
        print('------------------------')
        print('Version: {0}'.format(system.version))
        print('User ID: {0}'.format(system.account.user_id))
        print('Access Token: {0}'.format(system.account.access_token))
        print('Refresh Token: {0}'.format(system.account.refresh_token))

        events = await system.get_events()
        print('Number of Events: {0}'.format((len(events['events']))))

        print()
        print('Sensors:')
        for serial, sensor_attrs in system.sensors.items():
            print(
                '{0}: {1} ({2}) -> {3}'.format(
                    serial, sensor_attrs.name, sensor_attrs.type,
                    sensor_attrs.triggered))

        print()
        print('Refreshing Access Token:')
        await system.account.refresh_access_token()
        print('Access Token: {0}'.format(system.account.access_token))
        print('Refresh Token: {0}'.format(system.account.refresh_token))

        print()
        print('Setting System to "Home":')
        await system.set_home()
        await asyncio.sleep(5)

        print()
        print('Setting System to "Off":')
        await system.set_off()

    print()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        try:
            print()
            await exercise_client('EMAIL', 'PASSWORD', websession)
        except SimplipyError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
