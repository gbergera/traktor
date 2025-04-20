from . import driverinfo,balls,printer, drivers, constructors, help, calendar, gpresults, gpinfo, simplylovely, seasonschedule

def register_all_commands(client):
    print("Registering commands...")
    driverinfo.setup(client)
    drivers.setup(client)
    constructors.setup(client)
    help.setup(client)
    calendar.setup(client)
    gpresults.setup(client)
    gpinfo.setup(client)
    simplylovely.setup(client)
    seasonschedule.setup(client)
    balls.setup(client)
    printer.setup(client)