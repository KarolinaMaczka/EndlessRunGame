result= [{'emotion': {'angry': 0.6174157839268446, 'disgust': 2.279909523394963e-05, 'fear': 9.178365021944046, 'happy': 0.6296064238995314, 'sad': 16.482505202293396, 'surprise': 0.3967456053942442, 'neutral': 72.6953387260437}, 'dominant_emotion': 'neutral', 'region': {'x': 283, 'y': 177, 'w': 131, 'h': 158, 'left_eye': (384, 236), 'right_eye': (322, 241)}, 'face_confidence': 1.0}]

# print(result[0]['emotion'])
print(result[1])

# dominant_emotion = max(result['emotion'], key=result['emotion'].get)
# second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]