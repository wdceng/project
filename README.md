# Welding Book Database
#### Video Demo:  <URL HERE>
#### Description:
WeldDB (Welding Book Database) is a streamlined application designed to efficiently insert and manage weld data in a structured database. It helps welding professionals record, track, and organize weld inspections with ease and accuracy.

#### Git, Github, Docker and VSC Live Server extension:
While exploring Git and GitHub for version control, I came across Docker as a tool for managing dependencies and ensuring consistent environments. It felt like a natural next step to dive into Docker, especially to avoid the classic "It works on my machine" issues. I started by creating a Dockerfile and building containers for my app. Along the way, I discovered Gunicorn as a more production-ready alternative to flask run, which helped me better understand the differences between development and deployment environments.

Setting up the server and managing requirements.txt was quite a challenge at first. I learned that I didn’t need to install dependencies locally — Docker could handle everything within the container. I also ran into some issues, like reading from and writing to files across different paths, especially between the app directory and the root folder. Solving these problems helped deepen my understanding of Docker and deployment practices.

However, I found that constantly building Docker images and managing containers was slowing down my front-end development with HTML, CSS, and JavaScript. To streamline the process during the design phase, I started using a simple standalone file, dev.html, linked to the app's CSS and JS files. I ran it with the Live Server extension, which gave me instant feedback and significantly sped up my workflow while working on layout and styling.
