# F1 Manager Game
#### Video Demo:  (https://youtu.be/8a6fkGuI_Wc)
#### Description: Hello F1 Lovers & CS50 people! This project is created by SHRESTHA HARDIA, an aspiring Computer Science student, as his final CS50 project. This is a flask framework based web-app F1 Manager Game with focus on F1 strategies, car customization and real-time players competition. Built with FLASK and SQLAlchemy for backend, implements user authetication and session management for personalized experience/gameplay. Uses JINJA2 templates for responsive HTML rendering. Integrated APIs like: DEEPSEEK-API: for bot responses; F1 API for displaying real-world F1 standings. CSS and JavaScript used for responsive front-end and UI.

#### Effort made by developer to enhance F1 knowledge among F1 viewers.
##### I would like to THANK HARVARD-CS50 team for helping me to gain knowledge, throughout this Hardvard-CS50X course, required to build such dynamic web-app.

Code Explanantion:
1. App.py: It handles Backend & Server. Iit handles routes, HTML template rendering with data, Connects SQLAlchemy to register and store user data, implements logic such as match simulation; DEEPSEEK-API management; leaderboard, f1 standings and transfer page.

2. HTML files: These files are stored in templates folder used for building front-end of site using Jinja2-based HTML. Navbar.HTML is a template of Navbar which is later implemented in each page using Jinja2 and pages like Login.html, Register.HTML, Index.html and etc builds structure of each feature and are well linked with database by routing methods in APP.py.

3. Styles.css: Its a CSS file used for enhancing User-Interface of webapp by having basic features like Background Image slideshow, Text styles, page alignments and other css features. Its stored in Static folder.

4. F1user.db: This file is stored in Instance folder which consists user data like: Login Credentials, Game Progress and etc.

TODO/User Manual:
1. LOGIN & REGISTRATION : New Players first register themselves (here they chose their Username and Password) from REGISTER option in LOGIN Page then user will redirect to Login Page and put their login credentials to enter the game.

2. IN-GAME FEATURES: After Login player will enter to their user-specific dashboard where user can do multiple things like:
2.1.1 Selecting Racing circuit from the drop-down list and then creating Customized car setup like wing balance, suspension and break balance according to the specific circuit based on real-world tactics.
2.1.2 Later on they have to choose their pit-stop setup just like the above step.
2.1.3 Then player move towards match Lobby where their car setup competes with bot-car setup and best setup among them win and if player win they receive 1 trophy which directly credit into their user account after every win.

3. Wins and Trophies: Players can see their number of wins and trophies in top of the racing container and they can use these trophies to buy some f1-drivers listed in the Transfer page to improve/upgrade their team.

4. Leaderboard: Players can refer to LEADERBOARD page to see current Leading standings (among all users) based on the decreasing order of trophies.

5. REAL WORLD F1-STATS: Players can also refer to current season F1-Standings through LIVE F1 STANDINGS page and past seasons' stats through HISTORICAL STANDINGS page.

6. PROFILE FEATURES: Players can see their user-specific things like Trophies & Drivers by just clicking on their Username drop-down at Navbar which also include few essential features like: Password Change, Rename Username, DELETE ACCOUNT and LOGOUT.

NOTE: This is the initial version of this project and their will be some changes made by developer (Shrestha Hardia) in future so please stay tuned and if you spot any bug or issue please let developer know about it via EMAIL: hardiashrestha@gmail.com .

