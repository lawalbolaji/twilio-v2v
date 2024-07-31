from fastapi import APIRouter, Form, Request
from fastapi.responses import PlainTextResponse
from groq import APIConnectionError, APIStatusError, RateLimitError
from twilio.twiml.voice_response import VoiceResponse
from twilio.request_validator import RequestValidator

from app.config.config import Settings
from app.lib.groq import GroqClient
from app.lib.model import Model

router = APIRouter(prefix="/voice", default_response_class=PlainTextResponse)
model = GroqClient()

settings = Settings()


@router.post("/answer")
async def answer_call(req: Request):
    """Respond to incoming calls"""

    if not (await validate_request_from_twilio(req)):
        print("request is not from twilio")

    # build twiml flow
    twiml = VoiceResponse()
    twiml.say("Hello, I am Twilio voice assistant. What can I do for you today?")
    twiml.gather(action="/voice/ivr", input="speech", speech_timeout="2")
    twiml.say(
        "You can give us a call back any time"
    )  # fallback if user does not provider any input from preceding gather

    return str(twiml)


async def validate_request_from_twilio(req: Request):
    """validate that the request is from twilio"""

    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    _form = await req.form()

    return validator.validate(
        str(req.url), _form, req.headers.get("X-Twilio-Signature", "")
    )


def get_llm_response(model: Model, query: str):
    return model.complete(query)


@router.post("/ivr")
async def interactive(req: Request, SpeechResult: str = Form(...)):
    """handle interactive voice response"""

    if not (await validate_request_from_twilio(req)):
        print("request is not from twilio")  # act accordingly

    twiml = VoiceResponse()
    try:
        llm_response = (
            get_llm_response(model, SpeechResult)
            or "I didn't catch that, could you try again."
        )
        twiml.say(llm_response)
        twiml.gather(action="/voice/ivr", input="speech", speech_timeout="2")
        twiml.say("it was great talking to you, goodbye!")  # fallback
    except (APIConnectionError, RateLimitError, APIStatusError):
        # how you handle this is up to you
        twiml.say(
            "it was great talking to you, goodbye!"
        )  # llm client fails e.g. token_context_window exceeded

    return str(twiml)


@router.post("/events")
async def events(req: Request):
    """collect events from active call"""

    if not (await validate_request_from_twilio(req)):
        print("request is not from twilio")

    _form = await req.form()
    print(_form)
