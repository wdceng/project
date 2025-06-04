# Welding Book/Log DataBase

#### Video Demo: <URL HERE>

Project Title: **Welding Book/Log Database**\
Name: **Davor Šercer (pr. Shertser)**\
GitHub Username: **wdceng**\
edX Usernames: **davor_shertser**\
City and Country: **Zagreb, Croatia**\
Date of Video Recording: **June 5, 2025**

#### Description:

WeldDB (Welding Book/Log Database) is a streamlined application designed to efficiently insert and manage weld data in a structured database. It helps welding professionals record, track, and organize weld inspections with ease and accuracy.

## New Skills Acquired and Topics Researched

#### CSS Flexbox Git, Github, Docker, Gunicorn

Through [W3Schools](https://www.w3schools.com/css/css3_flexbox.asp), I have strengthened my CSS skills, with a particular focus on Flexbox, which I now use effectively for creating responsive layouts. While exploring [Git and GitHub](https://youtu.be/NcoBAfJ6l2Q) for version control , I came across Docker as a tool for managing dependencies and ensuring consistent environments. It felt like a natural next step to dive into [Docker](https://youtu.be/pg19Z8LL06w), especially to avoid the classic "It works on my machine" issues. I started by creating a Dockerfile, with docker init CLI, and building containers for project app. Along the way, I discovered [gunicorn](https://gunicorn.org/) (green unicorn) as a more production-ready alternative to [flask](https://flask.palletsprojects.com/en/stable/), which helped me better understand the differences between development and deployment environments.

Setting up the server and managing `requirements.txt` was quite a challenge at first. I learned that I didn’t need to install dependencies locally — Docker could handle everything within the container. I also ran into some issues, like reading from and writing to files across different paths, especially between the app directory and the root folder. Solving these problems helped deepen my understanding of Docker and deployment practices.

#### VSC Live Server and why?

However, I found that constantly building Docker images and managing containers was slowing down my front-end development with HTML, CSS, and JavaScript. To streamline the process during the design phase, I started using a simple standalone file, `dev.html`, linked to the app's CSS and JS files. I ran it with the [Live Server](https://youtu.be/vQd_fxzCIs0?t=2151) extension, which gave me instant feedback and significantly speed up my workflow while working on layout and styling.

#### Open color

All colors used in this project are sourced from [Open Color](https://yeun.github.io/open-color/)—an open-source, UI-optimized color palette designed for fonts, backgrounds, borders, and more. According to the official website: _"Open Color provides consistent perceived brightness across its palette, even when colors share the same brightness level. This ensures readability and balance, making the UI both accessible and visually cohesive"._

## Design Choices

Given my analytical nature, I see myself more as a backend developer than a frontend one. Design has been a personal challenge for me. Many of the design decisions in this project were influenced by popular [udemy](https://www.udemy.com/course/design-and-develop-a-killer-website-with-html5-and-css3/learn/lecture/27512356) online teacher [Jonas Schmedtmann](https://jonas.io/resources/) whose resources and teaching helped guide the visual aspects of the interface.

#### Light and Dark Theme

This project supports both light and dark themes to enhance accessibility and user preference. Welding engineers often work in low-light or darker environments, which makes a dark theme more suitable and comfortable for extended use. The theme is implemented using CSS custom properties (variables) and toggled via a data-theme attribute on the `<body>` tag.

#### Picking Colors and ChatGPT support

Colors like orange, yellow and reddish tones are often associated with welding, so I chose orange as the accent color. The base colors are various shades of gray to maintain a neutral and balanced background. As a non-designer, choosing the right color shades was a challenge for me, and I relied significantly on ChatGPT to make color pick decisions based on Open Color palette.

## Project Files – Contents and Functionality

The project files include all source code, templates, and assets required to run the application. Key components:

#### Backend Code

Handles routing, logic, and database operations (e.g., written in Python/Flask).

1. 1 **`app.py`** file serves as the main entry point for the Flask web application. It imports necessary modules, initializes the Flask app, defines routes, handles HTTP requests, and starts the development server.

2. 2 **`helpers.py`** file contains utility functions that support the main application logic. These functions help keep the app.py clean and organized by separating reusable code

#### Frontend Templates

HTML files structured for rendering views with dynamic data.

3. 1 **`layout.html`** file serves as the base template for all other HTML pages in a Flask application. It defines the overall structure of app’s pages, such as the header, navigation, and footer. This way we don’t need to repeat app’ structure in every file.

4. 2 **`login.html`** file provides the user interface for logging into the application. It is a child template that extends layout.html and includes a form where users enter their username and password.

5. 3 **`register.html`** file provides the user interface for creating a new account. Like `login.html`, it extends layout.html and contains a form for users to enter their registration details.

6. 4 **`index.html`** file serves as the homepage or main dashboard of your application. It displays a list of recorded welds retrieved from the database and allows users to view the data in a structured format

7. 5 **`upload_weld_data.index`** file provides the user interface for uploading new weld data to the application. This template contains a form where users can input details for a weld record, such as drawing number, revision, spool number, weld number, welder information, inspection results, and more.

8. 6 **`flash.html`** file is a partial template included via `{% include "flash.html" %}`. It is responsible for rendering flash messages—temporary notifications used to inform the user about events such as errors, success, or info.

#### Static Assets

CSS, JavaScript, and image files for styling and interactivity.

9. 1 **`favicon`** file is the small icon displayed in the browser tab, bookmarks, and address bar. It helps users visually identify web app and enhances the branding of application.

10. 2 **`scripts.js`** file contains JavaScript code that adds interactivity and behavior to web application. It is linked in layout.html and enhances user experience by handling client-side logic. One key function it handles is toggling between light and dark themes based on user interaction.

11. 3 **`style.css`** file contains the core styling rules for entire web application. It defines how elements look and behave visually, ensuring a consistent and responsive user interface.

#### Configuration Files

requirements.txt, and others for environment setup and dependencies.

12. 1 **requirements.txt** file lists all the Python packages Flask application needs to run. It is used to install dependencies quickly and consistently, especially in virtual environments or Docker containers which I use for this project.

#### Database Schema

SQL scripts or migrations to set up and manage the database structure.

13. 1 **weld_db.db** file is a SQLite database that stores all the persistent data for Welding Book/Log application. Such as `users` and `welds` table.

## Academic honesty and using ChatGPT

This web application was entirely built by me, applying knowledge gained from CS50x and the additional online resources mentioned above. ChatGPT served as a coding assistant, providing advice and comments, troubleshooting help, and explanations of programming concepts; however, all design, code, and final implementation decisions are my own.

##### Note on language and writing:

As English is not my first language, I used ChatGPT to check my writing for typos and improve the wording, while ensuring that it did not add any content beyond what I originally wrote.
