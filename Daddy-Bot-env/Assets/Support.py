#Grabs the list of names and roles from the text files and returns them as lists
def Grab_Files():
    try:
        nameFile = open("Daddy-Bot-env/Assets/Names.txt", "r")
        names = nameFile.read()
        nameList = names.splitlines()
        nameFile.close()
    except:
        print("Error: Names.txt not found!")
    # Grab the list of roles from the text file
    try:
        roleFile = open("Daddy-Bot-env/Assets/Roles.txt", "r")
        roles = roleFile.read()
        roleList = roles.splitlines()
        roleFile.close()
    except:
        print("Error: Roles.txt not found!")

    return nameList, roleList

#Grab the token and URL for the Discord bot from the Private.txt file
def Parse_Private():
    try:
        with open("Daddy-Bot-env/Assets/Private.txt", "r") as tokenFile:
            lines = tokenFile.readlines()
        
        # Initialize a dictionary to hold the values
        values = {}
        for line in lines:
            # Skip lines that do not contain ' = '
            if ' = ' not in line:
                continue
            key, value = line.strip().split(' = ')
            values[key] = value.strip("'")
        
        # Extract token and URL from the dictionary
        token = values.get('Token')
        URL = values.get('URL')
        
        if token is None or URL is None:
            raise ValueError("Token or URL not found in file")
        
        return token, URL
    
    except Exception as e:
        print(f"Error reading file or parsing content: {e}")
        return None, None


    
