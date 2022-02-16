# Traveller's Journal - CS50x Final Project 2021

#### Video Demo:  https://youtu.be/JfSB3XC5Etg

## General Description of the project

Traveller's Journal is a simple Web Application built with Flask. It allows users to create an account and start their own personal journal. The journal they create is private, so nobody besides them can see the content inside.

After logging in the user sees the homepage with a heading and short paragraph encouraging to start journaling. Below is a button which directs user to a "Add new entry" page (also available in the navbar).

Adding a new entry is very simple - all you need to do is fill in a form with title and content fields and click "Add". The content field is also enhanced with a rich text editor (CKEditor), so that users can change the appearance of the text and even add pictures (by providing url, uploading from hard drive will be probably added in the future).

Journal entries are displayed on My Journal page. They are sorted by date posted in a descending order, so that the lastly added entry is being displayed at the top of the page.

Every entry has two buttons at the bottom - "Update" and "Delete". Thanks to this feature everything in the journal may be modified or even deleted. However, deletion of a journal entry is preceded by a warning, preventing users from accidentally deleting content they created.

## Structure and Design of Program

### Package structure

Firstly, I was trying to develop this app using a structure similar to CS50 Finance. However, I decided to use SQLAlchemy instead of CS50 SQL library, and quite quickly I ran into problems with circular import. It basically means that one python file is trying to import from another python file which has not been initialized yet because it needs to import something from the first file, and it creates kind of an infinite loop :)

So, following the advice of Corey Schafer, I changed the structure of my application, and turned it into a package that can be imported. Now, the whole application is located in a 'travel' directory and outside of this folder lives a file named run.py which imports the whole application. In the travel directory there is also an initialization file called __init__.py which tells Python that my 'travel' directory is a package. This file initializes my application and brings together different components such as SQLAlchemy, CKEditor, LoginManager, etc.

### Files

#### views.py

This file defines all the routes used in application.

#### helpers.py

Here I have put database models and forms classes.

#### users.db

This is a database file.

#### Templates

In this directory, I have templates for my webpages such as homepage, login, register, journal, etc. More on front-end in Web Design section.

### Forms

When it comes to forms used in my web app, I am importing field types and validators from wtforms and then I am creating classes for various forms used on the website. Having such a class allows me to create an instance of a form in the chosen route and then pass it into the template.

### Database

For now, I am using sqlite and SQLAlchemy. In future will probably switch to MySQL or Postgres. When it comes to setting up my database, firstly I have configured it by assigning SQLALCHEMY_DATABASE_URI and db variable. I also had my database models ready for User and Post (located in helpers.py). When I had all this, I opened my terminal and ran a db.create_all() query to create a database file.

### Web Design

I am using mainly Bootstrap with few CSS rules added by myself. I am also using a free Bootstrap template called Bootswatch Sketchy - https://bootswatch.com/sketchy/
Backgrounds and icons are from Flaticon and Freepik.
On the homepage I have also implemented a simple typewriter effect, based on the code I found here: https://www.w3schools.com/howto/howto_js_typewriter.asp

## Future Development

In the future, I want to add more features to the journal itself, e.g. pagination, uploading pics from hard drive and nice lightbox gallery attached to each journal entry. But also, I would love to develop this web app into something more like a Traveller's Hub - a tool for travellers planning a new journey. I was thinking about adding features like checking weather, currency converter, timezone calculator, etc.