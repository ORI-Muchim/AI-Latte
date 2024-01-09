def get_emotion_from_response(response):
    emotion = "neutral"
    if "섹스" in response:
        emotion = "supershame"
    
    return emotion
