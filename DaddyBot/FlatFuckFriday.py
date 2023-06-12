def isFlatFuckFriday():
    #If the day is a friday between 9am-10am then it is flat fuck friday so return true
    import datetime
    now = datetime.datetime.now()
    if now.weekday() == 4:
        #IT IS FLAT FUCK FRIDAY!
        return True
    else:
        return False#, and sadness :(