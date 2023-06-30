def isFlatFuckFriday():
    #If the day is a friday between 9am-10am then it is flat fuck friday so return true
    import datetime
    import pytz

    #Create a timezone object for Chicago/Central
    chi_tz = pytz.timezone('America/Chicago')

    #Get the current time in Chicago/Central timezone
    correctednow = datetime.datetime.now(chi_tz)

    #Check if it is Friday and between 9am-10am
    if correctednow.weekday() == 4 and correctednow.hour == 9:
        #IT IS FLAT FUCK FRIDAY!
        return True
    else:
        return False#, and sadness :(
