from . import driverinfo,balls,printer, drivers, constructors, help, calendar, gpresults, gpinfo, simplylovely, seasonschedule,cornergraph,gearshifts,positionchanges,qualifyingresults,trackspeed

def register_all_commands(client):
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
    cornergraph.setup(client)
    gearshifts.setup(client)
    positionchanges.setup(client)
    qualifyingresults.setup(client)
    trackspeed.setup(client)
    
    