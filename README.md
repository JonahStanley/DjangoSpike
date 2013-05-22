DjangoSpike
===========

This is a brief introduction into using Django for the first time.

This will also include a description of what we hope to accomplish in the project as well as a small breakdown of the design/implementaiton process.

Project:
Simple chat forum thing

Specs:

Users can log in and out

Users can register and change information

Users can post and delete their posts as well as see all posts

Users can view other user's profiles and their posts

*Maybe* Posts can be edited

*Complex* Posts can be replied to specifically.  i.e. Post 2: @1 you are wrong.  This creates a thread and can be followed.


In depth specs:

Users must be logged in at all times (other than log in and registration screen). Otherwise, redirect to login

User names are unique.

If user was deleted, posts are kept but indicated


Pages:

Log in page

Registration Page

Forum Page

Profile Page (view dependent) /user/jonah vs. /user/ian vs. /user/ (
defaults to logged in user)

Edit Profile Page (information depends on view) edit-profile

List Users Page (by username)


Database Tables:

User: Using given Django Users


Post:

-ID (unique autocreated)

-Text

-TimeStamp

-UserID


TESTING:

user can be created

user name can't be repeated

user can't access other pages whilst not logged in

user can log in

user can log out

user can post

user can delete own post

user can't delete other post

user can view profile

user can view other profiles

user can edit own profile

user can't edit other profiles

user can delete account

user can't delete other accounts



Division of Labor:
Log in Page-Jonah

Registration Page-Jonah

Forum Page-Ian

List Users Page-Ian

Edit Profile Page-Jonah

Profile Page-Ian