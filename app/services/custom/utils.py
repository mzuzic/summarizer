from app.constants import (HIGH_CONFIDENCE_THRESHOLD, MEDIUM_CONFIDENCE_THRESHOLD, 
                           HIGH_CONFIDENCE, MEDIUM_CONFIDENCE, LOW_CONFIDENCE)


def _get_confidence_str(confidence):
    if confidence >= HIGH_CONFIDENCE_THRESHOLD:
        return HIGH_CONFIDENCE
    if confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
        return MEDIUM_CONFIDENCE
    return LOW_CONFIDENCE
