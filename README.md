# Chatbots_with_Simple_AI: Dobby Cocktail Companion
## Design Brief
The goal of my project is to create a Discord chatbot called "Dobby" that will take on the persona of Dobby from the Harry Potter series and provide users with a fun, humanized interactive experience. Gradually narrow down the user's needs and make final recommendations through constant questioning. Allowing users to experience the cocktail selection process as fun, rather than a painful entanglement.

## Exploration
The user will activate the Dobby Bot using the specific keyword "$EnjoyCocktail". The system will ask the user if they are having a good day, and will then respond to each step of the user's feedback with a different option or question until a final suggestion is provided. If the user is still not satisfied with the final suggestion, the system will help the user provide feedback through a pop-up questionnaire, which will further help the bot learn and adapt.

## Key Features
Mood Analysis: Begin by asking the user about their mood to personalize the experience. Dobby will provide cocktail suggestions based on whether the user is feeling happy, relaxed, or down. Cocktail Selection: Based on the mood input, Dobby will present a decision tree that narrows down cocktail choices through a series of questions about base spirit preferences (vodka, whiskey, absinthe, gin, tequila, rum). Interactive Dialogue: The chatbot will use language and phrases reminiscent of Dobby from Harry Potter, making the interaction delightful and thematic.

## Technologies used
The Dobby chatbot for this project will be activated on Discord through specific commands and will be built based on Discord's Python API. The interactive features of the bot will be realized by using the discord.py library to create a decision tree that can dynamically respond to user choices by building a Node class structure. To enhance the user experience, we will leverage the UI components provided by Discord, such as buttons and modal dialogs, to create an intuitive and interactive interface.

## Decision Tree
<img width="613" alt="Screenshot 2024-04-19 at 12 56 49" src="https://github.com/VilmaHE0601/Chatbots_with_Simple_AI/assets/146425185/e5f9776a-92cd-452d-b8e5-b23fe1db5382">

