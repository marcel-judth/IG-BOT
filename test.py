import instaloader
L = instaloader.Instaloader()
username = 'lenson_cricket'
password = 'LenDomik2201'
# Login or load session
L.login(username, password)        # (login)


# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, "prada")

# Print list of followees


file = open("prada_followers.txt","a+")
for followee in profile.get_followers():
    username = followee.username
    file.write(username + "\n")
    print(username)

file.close()