# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#
#
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


class ActionUserName(Action):

    def name(self) -> Text:
        return "action_ask_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {

        }
        dispatcher.utter_message(response="utter_user_name")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionUserNumber(Action):

    def name(self) -> Text:
        return "action_ask_user_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {

        }
        # dispatcher.utter_message(text="What is your contact number?")
        dispatcher.utter_message(
            message="What is your contact number?", response="utter_user_number")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionUserDetails(Action):

    def name(self) -> Text:
        return "action_display_user_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {
            "PERSON": tracker.get_slot("PERSON"),
            "number": tracker.get_slot("number"),
        }
        # dispatcher.utter_message(text="What is your contact number?")
        dispatcher.utter_message(response="utter_user_number_display")

        return [SlotSet(slot, value) for slot, value in slots.items()]
