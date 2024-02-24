import discord
from discord.ui import View, Button, Modal, TextInput
import os


## 1. Create Node Class
class Node:

  def __init__(self, value, answer="", children=[]):
    self.value = value
    self.answer = answer
    self.children = children
    #setup the Node
    # every node has a value, answer, and a childre, but in default they are defined to be empty


### 2. Create an Example Decision Tree
node1 = Node('Do Project', answer='Yes')
node2 = Node('Sleep', answer='No')
node3 = Node('Dobby is free! 🎉')
node4 = Node('"Oh! Dobby must not say!"', answer='No', children=[node1, node2])
node5 = Node('a')
node6 = Node('b')
node7 = Node('c')
node8 = Node('Dobby', answer='Maybe', children=[node5, node6, node7])
root = Node(
  'Dobby feels that the sunshine is especially warm today. Master, do you have any plans for today?', children=[node1, node4, node8])


## 3. Create GuessOptionsView Class
class GuessOptionView(View):

  def __init__(self, node):
    super().__init__()
    for child in node.children:
      self.add_item(GuessButton(child))
    #setup the GuessOptionsView

  async def handleButtonPress(self, interaction, node):
    if (node.children == []):
      # make a guess
      await interaction.response.send_message(
        content=f'Is the animal you are thinking of...{node.value}',
        view=WrongView(node))
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
    self.newAnimal = TextInput(label="What animal were you think of?")
    self.newQuestion = TextInput(
      label="A question to distinguish from the guess?")
    self.oldAnswer = TextInput(label="What answer gets to the guess?")
    self.newAnswer = TextInput(label="What answer gets to your animal?")
    self.add_item(self.newAnimal)
    self.add_item(self.newQuestion)
    self.add_item(self.oldAnswer)
    self.add_item(self.newAnswer)
    self.node = node

  async def on_submit(self, interaction):
    newNode1 = Node(self.node.value, answer=self.oldAnswer.value)
    newNode2 = Node(self.newAnimal.value, answer=self.newAnswer.value)
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

  if message.content.startswith('Hi, Dobby! How is it going?'):
    await message.channel.send(content=root.value, view=GuessOptionView(root))
    # root here is the node passed into the guessoptionview()


token = os.getenv("DISCORD_BOT_SECRET")
client.run(token)
