import os, webbrowser

credentialsFP = "{}//credentials//tokenFile.txt".format(os.getcwd())

# Function that reads the contents of the tokenFile stored in /credentials/ and returns the contents as a string 
def retrieveFromFile():
    api_token_file = open(credentialsFP, "r") 
	
    api_token = api_token_file.read()

    api_token_file.close()

    return api_token


def retrieveFromWeb():
    api_token = ""
    webbrowser.open("https://westernsydney.humanity.com/app/admin/apiv2/client_id=a3e3febe12a3375f4e66af282bb05db71be0c4f2/")
    return api_token


# Function that takes a string as a parameter and writes it to the credentials file
def storeCredentials(cred):
    api_token_file = open(credentialsFP, "w") 

    api_token_file.write(cred)

    api_token_file.close()

