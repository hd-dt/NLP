# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType, SlotSet, AllSlotsReset

class ValidateDinoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_dino_form"

    def dino_names_db(self) -> List[Text]:
        dino_names_org = pd.read_csv("C:/Users/hddt/NLP/data/dino_names_ls.csv")
        dino_names_ls = []
        for dino_name in dino_names_org:
            dino_names_ls.append(dino_name.lower())
        return dino_names_ls

    def validate_dino_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        lower_dino_names = self.dino_names_db()

        if slot_value.lower() in lower_dino_names:
            return {"dino_name": slot_value.capitalize()}
        else:
            dispatcher.utter_message(response = "utter_wrong_dino_name")
            test_name = slot_value.lower()
            match_dino_ls = ""
            match_ratio_ls = process.extractBests(test_name, lower_dino_names, limit=3, score_cutoff=75)
            print(match_ratio_ls)
            if len(match_ratio_ls) >0:
                buttons = []
                for dino in match_ratio_ls:
                    #match_dino_ls = "-" + match_dino_ls + dino[0].capitalize() + "\n"
                    payload = "/inform{\"dino_name\": \""+ dino[0].capitalize()+"\"}"
                    buttons.append({"title":"{}".format(dino[0].capitalize()), "payload": payload})
                buttons.append({"title":"None", "payload": "/not_match"})
            #dispatcher.utter_message(text = match_dino_ls)
                dispatcher.utter_message(text = "But I found some similar names. Do you mean ..." , buttons= buttons)
            else:
                dispatcher.utter_message(response="utter_check_dino_name")
            return {"dino_name": None}
#
class AskForDinoNameAction(Action):
    def name(self) -> Text:
        return "action_ask_dino_form_dino_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict,
        ) -> List[EventType]:
        try:
            template = tracker.events[-3]["metadata"]["utter_action"]
        except:
            template = None
        print(template)
        if template != "utter_wrong_dino_name":
            dispatcher.utter_message(response="utter_ask_dino_form_dino_name")
        #else:
        #    dispatcher.utter_message(response="utter_check_dino_name")
        return []

class ActionBriefDino(Action):
    def name(self) -> Text:
        return "action_brief_dino"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dino_name = tracker.get_slot("dino_name")
        URL = "https://dinosaurpictures.org/" + dino_name.capitalize() + "-pictures"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        text = "Quick facts about "
        facts_list = soup.find_all(lambda tag: tag.name == "p" and text in tag.text)
        response_text = ""
        for fact in facts_list:
            for f in fact.find_all("li"):
                response_text = response_text + "- " + f.text +"\n"
        dispatcher.utter_message(text=response_text)
        return [AllSlotsReset()]
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
