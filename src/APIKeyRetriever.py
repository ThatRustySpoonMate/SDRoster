import os, webbrowser


# Function that reads the contents of the tokenFile stored in /credentials/ and returns the contents as a string 
def retrieveFromFile():
    api_token_file = open("{}\\credentials\\tokenFile.txt".format(os.getcwd())) 
	
    api_token = api_token_file.read()

    return api_token


def retrieveFromWeb():
    api_token = ""
    webbrowser.open("https://westernsydney.humanity.com/app/admin/apiv2/client_id=a3e3febe12a3375f4e66af282bb05db71be0c4f2/")
    return api_token

