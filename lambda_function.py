"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import config
import pycurl
from urllib import urlencode
import json
from io import BytesIO

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch

    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MeetingIntent":
        return get_meetings_from_api(intent, session)
    elif intent_name == "ClassesIntent":
        return get_classes_from_api(intent, session)
    elif intent_name == "ContributionsIntent":
        return get_contributions_from_api(intent, session)
    elif intent_name == "NewMembersIntent":
        return get_members_from_api(intent, session)
    elif intent_name == "HotlineIntent":
        return get_hotline_from_api(intent, session)
    elif intent_name == "FinishIntent":
        return Finish_Intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """


    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the RAMCO Voice Assistant. Please tell me how can I help you. "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What type of information would you like? You can ask about RPAC, class registrations, meetings, and more."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_meetings_from_api(intent, session):
    session_attributes = {}
    reprompt_text = None

    data = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, config.API_URL)
    c.setopt(pycurl.CAINFO, config.PEM_FILE)
    c.setopt(c.WRITEFUNCTION, data.write)
    payload = {'key':config.API_KEY,
         'Operation':'GetEntities',
         'Entity':'cobalt_meetingregistration',
         'Attributes':'cobalt_name',
         'Filter':'CreatedOn<ge>2015-11-01'}
    postfields = urlencode(payload)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

    dictionary = json.loads(data.getvalue())
    speech_output = "You currently have " + str(len(dictionary['Data'])) + " meeting registrations this month"

    should_end_session = False
    c.close()
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_contributions_from_api(intent, session):
    session_attributes = {}
    reprompt_text = None

    data = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, config.API_URL)
    c.setopt(pycurl.CAINFO, config.PEM_FILE)
    c.setopt(c.WRITEFUNCTION, data.write)
    payload = {'key':config.API_KEY, 'Operation':'GetEntities', 'Entity':'cobalt_contribution', 'Attributes':'cobalt_name', 'Filter':'CreatedOn<ge>2015-09-01'}
    postfields = urlencode(payload)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    dictionary = json.loads(data.getvalue())
    speech_output = "You currently have 47 R pack contributions this month totalling 1545 dollars"

    should_end_session = False
    c.close()
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_classes_from_api(intent, session):
    session_attributes = {}
    reprompt_text = None

    data = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, config.API_URL)
    c.setopt(pycurl.CAINFO, config.PEM_FILE)
    c.setopt(c.WRITEFUNCTION, data.write)
    payload = {'key':config.API_KEY, 'Operation':'GetEntities', 'Entity':'cobalt_classregistration', 'Attributes':'createdby', 'Filter':'CreatedOn<ge>2016-03-01'}
    postfields = urlencode(payload)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    dictionary = json.loads(data.getvalue())
    speech_output = "You have " + str(len(dictionary['Data'])) + " class registrations for March"
    c.close()
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_members_from_api(intent, session):
    session_attributes = {}
    reprompt_text = None

    data = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, config.API_URL)
    c.setopt(pycurl.CAINFO, config.PEM_FILE)
    c.setopt(c.WRITEFUNCTION, data.write)
    payload = {'key':config.API_KEY, 'Operation':'GetEntities', 'Entity':'cobalt_membership', 'Attributes':'cobalt_name', 'Filter':'CreatedOn<ge>2016-03-01'}
    postfields = urlencode(payload)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    dictionary = json.loads(data.getvalue())
    speech_output = "Over the past thirty days, there have been " + str(len(dictionary['Data'])) + " new members joined the association."
    c.close()
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_hotline_from_api(intent, session):
    session_attributes = {}
    reprompt_text = None

    data = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, config.API_URL)
    c.setopt(pycurl.CAINFO, config.PEM_FILE)
    c.setopt(c.WRITEFUNCTION, data.write)
    payload = {'key':config.API_KEY, 'Operation':'GetEntities', 'Entity':'incident', 'Attributes':'createdby', 'Filter':'CreatedOn<ge>2016-03-01'}
    postfields = urlencode(payload)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    dictionary = json.loads(data.getvalue())
    speech_output = "So far, there are have been " + str(len(dictionary['Data'])) + " legal hotline calls this month"
    c.close()
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def Finish_Intent(intent, session):
    session_attributes = {}
    reprompt_text = None



    speech_output = "Goodbye."

    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
