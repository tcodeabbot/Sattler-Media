# Sadler Media Design Document

## Introduction
It allows users to create accounts, share posts with text and images, view posts from other users, receive notifications about new posts, and interact with the content. This document provides a technical overview of the project's implementation, discussing the design decisions made and the rationale behind them.

## Technologies Used
- Python with Flask Framework: Flask was my choice for building the web application, handling routing, and managing requests and responses.
- SQLite Database: I used SQLite to store user data, posts, and other information required by the application.
- HTML, CSS, and JavaScript: These front-end technologies helped me create the user interface and then style pages.
- Jinja Templates: Jinja templates played a crucial role in generating dynamic HTML content based on data from the backend.

## Design Overview
### Backend Structure
I structured the backend of Sattler Media using Flask, defining routes for various functionalities such as user authentication, post creation, and profile viewing. The application utilizes a SQLite database to store user information, including usernames, passwords, email addresses, bios, profile pictures, and posts.

### User Authentication
For user authentication, I implemented Flask's session management and password hashing utilities. When a user registers or logs in, their credentials are validated against entries in the SQLite database. Passwords are securely hashed using the `generate_password_hash` which I used from CS50's finance project, and hashed passwords are stored in the database. During login, passwords are checked using the `check_password_hash` function to ensure secure authentication.

### Post Creation and Viewing
Users can create new posts containing text and optional images. When a user creates a post, the text content and image (if provided) are stored in the SQLite database, along with metadata such as the user ID, post date, and post ID. Posts are displayed on the home page, allowing users to view and interact with them. Post images are uploaded to the server and stored in the `static/uploads/` directory. I did this decision to store the actual images in a directory in the workspace because when redering the imgae on the page, the I needed a file path so I had to store a file path in the database such that upon appearing in the HTML/jinja markup, the image for the particular post can easily showup on the page.

### Notifications
To notify users about new posts from other users, the application employs a simple notification mechanism. When a user logs in or visits the home page, the application queries the database for new posts since the user's last visit and displays them as notifications. Notifications include details such as the post author, post ID, and post date.

## Design Decisions

### Separation of Concerns
To maintain clean code, I followed the principle of separation of concerns. I used Flask's MVC (Model-View-Controller) architecture. Templates are used for rendering HTML pages, while routes handle backend logic such as database queries and session management.

### Scalability and Flexibility
I designed the project to be scalable and flexible, allowing for easy addition of new features and enhancements in the future. By separating concerns and following best practices in Flask development, the application codebase remains organized and extensible.

### Security Considerations
Security was a top priority in my design. Passwords are securely hashed before storage to prevent unauthorized access to user accounts. Additionally, session management was implemented to prevent common web security vulnerabilities.

## Conclusion

Sattler Media is designed with simplicity, scalability, and security in mind. By leveraging Flask and SQLite, the application provides a robust platform for social media interaction while ensuring a smooth and secure user experience.

## Thanks you

