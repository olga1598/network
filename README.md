# CS50’s Web Programming with Python and JavaScript


## Project 4. Network.


A Twitter-like social network website for making posts and following users.

### Specification


Using *Python*, *JavaScript*, *HTML*, and *CSS*, completed the implementation of a social network that allows users to make posts, follow other users, and “like” posts.

* **New Post**: Users who are signed are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post. 
* **All Posts**: The “All Posts” link in the navigation bar takes the user to a page where he/she can see all posts from all users, with the most recent posts first. 
* **Profile Page**: Clicking on a username should load that user’s profile page. 
    * Displasy the number of followers the user has, as well as the number of people that the user follows.
    * Display all of the posts for that user, in reverse chronological order.
    * For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. This only applies to any “other” user: a user is not able to follow himself.
* **Following**: The “Following” link in the navigation bar takes the user to a page where he/she can see all posts made by users that the current user follows. 
* **Pagination**: On any page that displays posts, posts only are displayed 10 on a page. If there are more than ten posts, a “Next” button appears to take the user to the next page of posts (which is older than the current page of posts). If not on the first page, a “Previous” button appears to take the user to the previous page of posts as well.  
* **Edit Post**: Users are able to click an “Edit” button or link on any of their own posts to edit that post. 
* **“Like” and “Unlike”**: Users areable to click a button or link on any post to toggle whether or not they “like” that post. 


### To Run the App

Open your code editor and in terminal go to the folder where you copies the code and run the following commands:

```
python manage.py makemigrations
python manage.py migrate
```

Now you can run your server:

`python manage.py runserver`


