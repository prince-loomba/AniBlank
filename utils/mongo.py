cards_collection = db.cards

# Define the card data
cards_data = cards_data = [
  {
      'location': 1,
      'floor': 1,
      'name': 'Sora',
      'talent': 'Brilliant Tactics',
      'talent_description': 'Reduces enemy defense by 10% and increases all allies’ attack by 10%.',
      'card_id': 1,
      'hp': 70,
      'atk': 90,
      'def': 90,
      'spd': 100,
      'quote': '“Life is not a game of luck. If you wanna win, work hard.”',
      'image': 'https://avatarfiles.alphacoders.com/305/305561.jpg'
  },
  {
      'location': 1,
      'floor': 2,
      'name': 'Shiro',
      'talent': 'Perfect Calculation',
      'talent_description': 'Achieves a critical hit 100% of the time.',
      'card_id': 2,
      'hp': 100,
      'atk': 85,
      'def': 80,
      'spd': 75,
      'quote': '“Chess is no different than tic-tac-toe.”',
      'image': 'https://static.zerochan.net/Shiro.%28No.Game.No.Life%29.full.2597656.jpg'
  }
]

# Insert the data into the collection
result = cards_collection.insert_many(cards_data)
print(f'Inserted {len(result.inserted_ids)} cards into the collection.')