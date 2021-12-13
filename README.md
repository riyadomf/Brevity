# Brevity
### <b>A blog site made for experience and resource sharing.</b>
<br/>

## Motivation
This is a blog site where experienced people can share their knowledge and the difficulties they faced while learning a particular topic. Beginners can ask for resources and seek help from experts. It will connect beginners with experts.   
Currently most of us use Facebook for this purpose which is overwhelming and distracting. Brevity means precise and exact use of words. It will always encourage to the point discussion.  

## Features Implemented
* A Responsive UI for users
* User Authentication
  * Login, Register 
  * Password Reset
* User Profile
  * Update Profile 
* Post 
  * CRUD operation
  * Upvote, Downvote 
  * Comment 
    * Anyone can Comment 
    * can be deleted by Post Author and Comment Author
  * Resource 
    * Post Author can Upload files with valid extensions (within specified size) 
    * Anyone can Download Resource files from post
  * Users can Bookmark their favourite posts
  * Tag
    * Users can assign specific Tags to their post
    * Update Tag
   
* Search Post with 
  * Title
  * Tag (using 3rd bracket)
  * Admin defined Tag (e.g. If user searches with [dbms] tag then search results will contain posts of [dbms] tag along with [database] tag)  
 
* Sort Post
  * by Date
  * by Popularity 
  * on search results
* User Contribution
  * based on Upvote, downvote
  * Top Contributors list
* Create/Edit post content using Rich text editor
  * Create Table
  * Insert image by url
  * various font styles 
  * Numbered/Bulleted list


* More Features:
  * Infinite scroll and lazy loading 
  * One can see all post of a particular user by clicking on his/her username
  * User summary in a popup panel when hovering over the user's name

## Used Technologies
*  Framework: Flask
*  Language: Python
*  Database: MySQL
*  Frontend: HTML, CSS, JavaScript, HTMX