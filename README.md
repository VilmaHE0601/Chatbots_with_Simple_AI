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

# Create GuessOptionsView Class
```
class GuessOptionView(View):

  def __init__(self, node):
    super().__init__()
    for child in node.children:
      self.add_item(GuessButton(child))
    #setup the GuessOptionsView

  async def handleButtonPress(self, interaction, node):
    if (node.children == []):
      if (node.good_result == False):
        # make a guess
        await interaction.response.send_message(content=f'Hmm...{node.value}',
                                                view=WrongView(node))
      else:
        await interaction.response.send_message(content=node.value)

    else:
      await interaction.response.send_message(content=node.value,
                                              view=GuessOptionView(node))
```

# Create GuessButton
```
class GuessButton(Button):

  def __init__(self, node):
    super().__init__(label=node.answer)
    self.node = node
    #setup the GuessButton

  async def callback(self, interaction):
    await self.view.handleButtonPress(interaction, self.node)
```

# Create WrongView
```
class WrongView(View):

  def __init__(self, node):
    super().__init__()
    self.node = node
    #setup the WrongView
  @discord.ui.button(label="Wrong")
  async def buttonCallback(self, interaction, button):
    await interaction.response.send_modal(FeedbackModal(self.node))
```

# Create FeedbackModal
```
class FeedbackModal(Modal, title="Feedback"):

  def __init__(self, node):
    super().__init__()
    self.newCocktail = TextInput(label="Describe your mood today?")
    self.newQuestion = TextInput(label="Describe your favorite flavor?")
    self.oldAnswer = TextInput(label="Enter a base wine?")
    self.newAnswer = TextInput(label="Enter the name of this cocktail?")
    self.add_item(self.newCocktail)
    self.add_item(self.newQuestion)
    self.add_item(self.oldAnswer)
    self.add_item(self.newAnswer)
    self.node = node

  async def on_submit(self, interaction):
    newNode1 = Node(self.node.value, answer=self.oldAnswer.value)
    newNode2 = Node(self.newCocktail.value, answer=self.newAnswer.value)
    self.node.value = self.newQuestion.value
    self.node.children = [newNode1, newNode2]
    await interaction.response.send_message(
      f'Thanks for updating the algorithm {self.node.value}')
```

# Run the Discord Bot
```
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$EnjoyCocktail'):
    await message.channel.send(content=root.value, view=GuessOptionView(root))
    # root here is the node passed into the guessoptionview()


token = os.getenv("DISCORD_BOT_SECRET")
client.run(token)
```

## Outcome
<img width="634" alt="Screenshot 2024-04-19 at 13 14 03" src="https://github.com/VilmaHE0601/Chatbots_with_Simple_AI/assets/146425185/708d9595-2728-4319-aee7-56eaa4621366">
<img width="721" alt="Screenshot 2024-04-19 at 13 15 10" src="https://github.com/VilmaHE0601/Chatbots_with_Simple_AI/assets/146425185/8fcb2f29-7a05-4d14-afc6-43e8c3e42d61">
<img width="488" alt="Screenshot 2024-04-19 at 13 15 33" src="https://github.com/VilmaHE0601/Chatbots_with_Simple_AI/assets/146425185/161e085a-cc45-458c-8ebb-5f0b6fda1da9">

## Reflection
I first settled on Dobby as the main character for this Chatbot during the process, this is because I really like the character of Dobby the elf from Harry Potter, he is very loyal and cute. And I'm a person who struggles with what cocktail to drink every time, I think each cocktail has its own specific meaning and mood, so I thought it would be a good choice to combine the two. The biggest challenge I encountered in this process was how to avoid the "Wrong" button popping up every time there was no option, because I thought that after Dobby provided the correct option for the user, the user didn't need to provide feedback to the system. I added `good_result=True` to a few specific Nodes and added the following logic to the third part of the code: Create GuessOptionsView Class:

1. If the current node node has any children. If `node.children` is empty, it has reached the end of the decision tree.
2. If the end is reached and `node.good_result` is False, it means that this is not a good result. The bot will send a message prompting "Hmm..." plus the value of the current node, and show a WrongView view.
3. If `node.good_result` is True, the bot will simply send a message with the value of the node, which represents a correct or positive result.
4. If the current node has `children`, meaning that the decision tree is not yet finished, the bot will send a message displaying the value of the current node with a GuessOptionView view, which will contain further options for the user to choose from.

This ensures that the Wrong View view is no longer displayed when the user is satisfied with the suggestions made by Dobby.


