def get_next_card_id(db):
  # Find the document that holds the global card_id
  global_id = db.global_ids.find_one_and_update(
      {"_id": "card_id"},
      {"$inc": {"current_id": 1}},
      return_document=True
  )

  # If no document exists yet, create one
  if not global_id:
      db.global_ids.insert_one({"_id": "card_id", "current_id": 1})
      return 1
  return global_id['current_id']
