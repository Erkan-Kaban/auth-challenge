# Flask authentication challenge

The purpose of this challenge is to add authentication to the ripe tomatoes app. The provided code already has the db connection, Movie and Actor models and schemas, and the routes to get them.

- Clone/fork the repo.
- Create the virtual environment.
- Install the requirements with ```pip install -r requirements.txt```
- drop, create and seed the database with the provided cli commands.
- Run the app with ```flask run``` , and check the ```/movies``` and ```actors```

If everything works fine let's go with the tasks to set up the authentication:

- Create the user model (username and password).
- Create the user schema (password length at least 8 characters). Passwords meant to be stored in the database with a hash generated by bcrypt.
- Seed the database with one new user.
- Create the ```/auth/signup``` and ```/auth/signin``` POST routes to sign up and sign in users. The response of this requests should return a jwt token.
- Make sure new users are added to the database, with the hash password.
- Create POST and DELETE methods for Actors and Movies. The routes need to include an id parameter to find the items in the database. Only authenticated users are able to do this actions. Handle the wrong requests with meaningful messages for the user (not authenticated and wrong id)

Challenge completed when an authenticated user is able to create and delete movies and actors, but also when a non authenticated user is not allowed to do that.
