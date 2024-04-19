# Chatbots_with_Simple_AI: Dobby Cocktail Companion
## Design Brief
The goal of my project is to create a Discord chatbot called "Dobby" that will take on the persona of Dobby from the Harry Potter series and provide users with a fun, humanized interactive experience. Gradually narrow down the user's needs and make final recommendations through constant questioning. Allowing users to experience the cocktail selection process as fun, rather than a painful entanglement.

## Exploration
The user will activate the Dobby Bot using the specific keyword "$EnjoyCocktail". The system will ask the user if they are having a good day, and will then respond to each step of the user's feedback with a different option or question until a final suggestion is provided. If the user is still not satisfied with the final suggestion, the system will help the user provide feedback through a pop-up questionnaire, which will further help the bot learn and adapt.

## Key Features
Mood Analysis: Begin by asking the user about their mood to personalize the experience. Dobby will provide cocktail suggestions based on whether the user is feeling happy, relaxed, or down. Cocktail Selection: Based on the mood input, Dobby will present a decision tree that narrows down cocktail choices through a series of questions about base spirit preferences (vodka, whiskey, absinthe, gin, tequila, rum). Interactive Dialogue: The chatbot will use language and phrases reminiscent of Dobby from Harry Potter, making the interaction delightful and thematic.

## Technologies Used
The Dobby chatbot for this project will be activated on Discord through specific commands and will be built based on Discord's Python API. The interactive features of the bot will be realized by using the discord.py library to create a decision tree that can dynamically respond to user choices by building a Node class structure. To enhance the user experience, we will leverage the UI components provided by Discord, such as buttons and modal dialogs, to create an intuitive and interactive interface.

## Decision Tree
<img width="613" alt="Screenshot 2024-04-19 at 12 56 49" src="https://github.com/VilmaHE0601/Chatbots_with_Simple_AI/assets/146425185/e5f9776a-92cd-452d-b8e5-b23fe1db5382">

## Coding
# Create Node Class
```
class Node:

  def __init__(self, value, answer="", children=[], good_result=False):
    self.value = value
    self.answer = answer
    self.children = children
    self.good_result = good_result
```
# Create a Decision Tree
```
###Happy Relaxed Today
MojitoNode2 = Node(" ", answer="No")
MojitoNode1 = Node("Master has given Dobby a good choice!",
                   good_result=True,
                   answer="Yes")

TequilaSunriseNode2 = Node(" ", answer="No")
TequilaSunriseNode1 = Node("Weee!!", good_result=True, answer="Yes")

French75Node2 = Node(" ", answer="No")
French75Node1 = Node("Dobby is happy!", good_result=True, answer="Yes")

MojitoNode = Node("Mojito", answer="Rum", children=[MojitoNode1, MojitoNode2])
TequilaSunriseNode = Node("Tequila Sunrise",
                          answer="Tequila",
                          children=[TequilaSunriseNode1, TequilaSunriseNode2])
French75Node = Node("French 75",
                    answer="Gin",
                    children=[French75Node1, French75Node2])

option2b = Node("Dobby is freeeee!!!", good_result=True, answer="No")
option2a = Node("What base wine does master prefer?",
                answer="Yes",
                children=[French75Node, TequilaSunriseNode, MojitoNode])

###Feeling Down Today
AbsintheDripNode2 = Node(" ", answer="No")
AbsintheDripNode1 = Node(
  "Dobby doesn't like Absinthe Drip, but the master's preference is most important!",
  good_result=True,
  answer="Yes")

OldFashionedNode2 = Node(" ", answer="No")
OldFashionedNode1 = Node("Dobby loves Old Fashioned!",
                         good_result=True,
                         answer="Yes")

BlackRussianNode2 = Node(" ", answer="No")
BlackRussianNode1 = Node("Dobby likes Black Russian too!",
                         good_result=True,
                         answer='Yes')

AbsintheNode = Node("Absinthe Drip",
                    answer="Absinthe",
                    children=[AbsintheDripNode1, AbsintheDripNode2])
WhiskeyNode = Node("Old Fashioned",
                   answer="Whiskey",
                   children=[OldFashionedNode1, OldFashionedNode2])
VodkaNode = Node("Black Russian",
                 answer="Vodka",
                 children=[BlackRussianNode1, BlackRussianNode2])

option1b = Node("What base wine does master prefer?",
                answer="Yes",
                children=[VodkaNode, WhiskeyNode, AbsintheNode])
option1a = Node("Dobby will be here for you.", good_result=True, answer="No")

### Today's Mood
FeelingDownNode = Node(
  "Dobby wants to have a cocktail with master when you are feeling down.",
  answer="No",
  children=[option1a, option1b])
HappyRelaxedNode = Node(" Want a cocktail, master?",
                        answer="Yes",
                        children=[option2a, option2b])

root = Node("Does master feel happy or relaxed today?",
            children=[FeelingDownNode, HappyRelaxedNode])
```
