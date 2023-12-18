# Flask Blog API

## Developer Information
- **Name:** [Abhishek Shankar]
- **Stevens Login:** [20021387]
- **GitHub Repo:** [https://github.com/AbhishekShankar17/WebForum]

## Project Overview
This project is a simple Flask-based API for creating and managing blog posts and users. It provides various endpoints for user registration, post creation, retrieval, deletion, and searching.

## Time Spent
I spent approximately [8 -12] on this project.

## Testing
To test the code, you can use tools like [Postman](https://www.postman.com/) or simply use command-line tools like `curl`. Here are some basic testing instructions for each of the implemented extensions:

### Extension 1: User Registration
- **Endpoint:** `/createuser`
- **Method:** POST
- **Request Body:** JSON object with a "username" field.
- **Testing:** Send a POST request to `/createuser` with a valid JSON object containing a "username" field. Verify that a new user is created and returned in the response.

### Extension 2: Moderator Registration
- **Endpoint:** `/createmoderator`
- **Method:** POST
- **Request Body:** JSON object with a "username" field.
- **Testing:** Send a POST request to `/createmoderator` with a valid JSON object containing a "username" field. Verify that a new moderator user is created and returned in the response.

### Extension 3: Thread replies
- **Endpoint:** `/createpost`
- **Method:** POST
- **Request Parameter:** "parent_id"
- **Testing:** Send a post request to `/createpost` with a "parent_id" parameter to indicate that it is a reply to another post. Additionally, when returning information about a post, we include the parent_id if it is a reply and the IDs of every reply to that post.

### Extension 4: Delete Post with User Authorization
- **Endpoint:** `/deletepost/<int:post_id>`
- **Method:** DELETE
- **Request Body:** JSON object with "key" and "user_id" fields.
- **Testing:** Send a DELETE request to `/deletepost/<int:post_id>` with a valid JSON object containing "key" and "user_id" fields. Verify that the post is deleted only if the user is authorized.

### Extension 5: Thread Based range queries
- **Endpoint:** `/thread/<int:post_id>`
- **Method:** GET
- **Testing:** Send a GET request to `/thread/<int:post_id>` that accepts a post_id as a parameter. This endpoint retrieves the thread of posts that includes the specified post and its transitive reply chains, both up and down the hierarchy.

## Bugs and Issues
- [Currently, the user registration endpoints (/createuser and /createmoderator) do not perform validation on the uniqueness of usernames. Users with duplicate usernames can be created.]



