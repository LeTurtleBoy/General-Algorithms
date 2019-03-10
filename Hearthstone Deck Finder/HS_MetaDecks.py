import requests

r = requests.get("https://www.hearthstonetopdecks.com/hearthstones-best-standard-ladder-decks/")
Clases = r.text.split("entry-footer")[0].split("Tier 1 Decks")[1].split("<h2>")
Decks = Clases[1:len(Clases)]

for Deck in Decks:
    try:
        Name = Deck.split("</h2>")[0]
        Code = Deck.split("data-deck-code=\"")[1]
        Code = Code.split("\">")[0]
        print(Name, Code)
    except:
        print("------------------------------------")
