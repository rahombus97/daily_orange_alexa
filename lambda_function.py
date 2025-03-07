import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name

from ask_sdk_model.ui import StandardCard
from ask_sdk_model.ui.image import Image

from Headlines import HeadLines

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DAILY_ORANGE_LOGO = Image("https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Otto_the_Orange_logo.svg/1920px-Otto_the_Orange_logo.svg.png")

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to the Daily Orange skill, you can ask for the headlines!"

    return handler_input.response_builder.speak(speech_text).set_card(
        StandardCard("Daily Orange", speech_text, DAILY_ORANGE_LOGO)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("ReadHeadlinesIntent"))
def read_headlines_intent_handler(handler_input):
    """Handler for Read Headlines Intent."""
    # type: (HandlerInput) -> Response
    try: 
        speech_text = HeadLines().getHeadlines()
    except Exception as e:
        logger.error("An error occured: {e}")

    return handler_input.response_builder.speak(speech_text).set_card(
        StandardCard("Daily Orange", speech_text, DAILY_ORANGE_LOGO)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can ask for the headlines!"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(StandardCard(
            "Daily Orange", speech_text, DAILY_ORANGE_LOGO)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "See ya! Go Orange!"

    return handler_input.response_builder.speak(speech_text).set_card(
        StandardCard("Daily Orange", speech_text, DAILY_ORANGE_LOGO)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Daily Orange skill can't help you with that.  "
        "You can ask for the headlines!!")
    reprompt = "Want to ask for the headlines!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()