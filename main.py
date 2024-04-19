import discord
from discord.ui import View, Button, Modal, TextInput
import os


## 1. Create Node Class
class Node:

  def __init__(self, value, answer="", children=[], good_result=False):
    self.value = value
    self.answer = answer
    self.children = children
    self.good_result = good_result
    #setup the Node
    

### 2. Create a Decision Tree
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


## 3. Create GuessOptionsView Class
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

  #what should happen when a button is pressed?


## 4. Create GuessButton
class GuessButton(Button):

  def __init__(self, node):
    super().__init__(label=node.answer)
    self.node = node
    #setup the GuessButton

  async def callback(self, interaction):
    await self.view.handleButtonPress(interaction, self.node)
    #what happens when this button is pressed


## 5. Create WrongView
class WrongView(View):

  def __init__(self, node):
    super().__init__()
    self.node = node
    #setup the WrongView
  @discord.ui.button(label="Wrong")
  async def buttonCallback(self, interaction, button):
    await interaction.response.send_modal(FeedbackModal(self.node))


# 6. Create FeedbackModal
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
    #setup the FeedbackModal


## 7. Run the Discord Bot
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
