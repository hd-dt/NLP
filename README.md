# NLP
 Chatbot with Rasa
 This chatbot is based on the idea of "Tina the T-Rex" from National Geographic Kids. The aim is to inspire children to learn in a more active way about dinosaurs.
 The bot asks the name of interested dinosaur or user can initially tell it.
 
 After that Dino-Bot will validate the input using fuzzy-wuzzy package from seatgeek and a pre-defined list retrieved from https://dinosaurpictures.org/ with 1365 names of discovered dino types.
 If the input match with one item from the list, the relevant information of that dinosaur will be retrieved from the website https://dinosaurpictures.org/ with a picture and then they are showed to users.
 In case it does not match with any item in the list, but it has more than 75% similarity with at least one of item in the list, the bot will suggest these potential items to users as one of them can be the one user thinks of but misspells. Otherwise the bot informs to users that the input is not right ans ask them to check by themselves.
 
 Moreover, the bot can handle some trained out of scope requests and has a customized reaction to fallback cases. 
