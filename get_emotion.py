import random
import re

def get_emotion_from_response(response):
    emotion_keywords = {
        "슬픔": ["cry"],
        "증오": ["hate", "hate2", "hate3"],
        "웃음": ["laugh", "laugh2"],
        "부끄러움": ["littleshame", "shame", "supershame"],
        "걱정스러움": ["worry"],
        "실망": ["disappointed"],
        "중립": ["hmm", "normal"]
    }

    pattern = r'\[(.*?)\]'
    korean_emotions = re.findall(pattern, response)

    possible_emotions = []

    for emotion in korean_emotions:
        possible_emotions.extend(emotion_keywords.get(emotion, []))

    if "섹스" in response:
        return "supershame"

    return random.choice(possible_emotions) if possible_emotions else "normal"
