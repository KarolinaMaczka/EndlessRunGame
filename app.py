from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

API_KEY = ""
def insert_data_from_json(json_data):
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()

    score = json_data.get("score")
    player_satisfaction = json_data.get("player_satisfaction")
    playing_time = json_data.get("playing_time")

    cursor.execute('''INSERT INTO Game (score,player_satisfaction, playing_time) VALUES (?, ?,?)''', (score, player_satisfaction, playing_time))
    game_id = cursor.lastrowid

    for obstacle in json_data.get("obstacle_data", []):
        obstacle_name, position_z, lane = obstacle
        cursor.execute('''INSERT INTO Obstacles (game_id, obstacle_name, position_z, lane) values (?, ?, ?, ?)''', (game_id, obstacle_name, position_z, lane))

    for hit_obstacle in json_data.get("hit_obstacles", []):
        obstacle_name, side, hit_type, obstacle_position_z, obstacle_lane, player_position_x, player_position_y, player_position_z = hit_obstacle
        cursor.execute('''INSERT INTO HitObstacles (game_id, obstacle_name, side, hit_type, obstacle_position_z, obstacle_lane,player_position_x, player_position_y, player_position_z) values (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (game_id, obstacle_name, side, hit_type, obstacle_position_z, obstacle_lane, player_position_x,player_position_y, player_position_z))

    for map_data in json_data.get("map_data", []):
        map_type, lane_change_prob, small_obs_prob, gate_prob, color_theme, start, end, generation_dist = map_data
        cursor.execute('''INSERT INTO MapData (game_id, map_type, lane_change_prob, small_obs_prob, gate_prob, color_theme, start, end, generation_dist) values (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (game_id, map_type, lane_change_prob, small_obs_prob, gate_prob, color_theme, start, end, generation_dist))

    for emotions in json_data.get("player_emotions", []):
        first_emotion, first_emotion_value, second_emotion, second_emotion_value, player_z, face_confidence = emotions[0][0], emotions[0][1], emotions[1][0], emotions[1][1], emotions[2], emotions[3]
        cursor.execute('''INSERT INTO PlayerEmotions (game_id, first_emotion, first_emotion_value, second_emotion, second_emotion_value, player_z, face_confidence) values (?, ?, ?, ?, ?, ?, ?)''', (game_id, first_emotion, first_emotion_value, second_emotion, second_emotion_value, player_z, face_confidence))

    for difficulty in json_data.get("difficulties", []):
        cursor.execute('''INSERT INTO Difficulties (game_id, difficulty_level) values(?, ?)''', (game_id, difficulty))

    for keys in json_data.get("keys_pressed", []):
        key_type, player_z = keys
        cursor.execute('''INSERT INTO KeysPressed (game_id, key_type, player_z) values (?,?, ?)''', (game_id, key_type, player_z))

    print(f"inserted data game id {game_id}")
    connection.commit()
    connection.close()

@app.route('/player-data', methods=['POST'])
def receive_data():
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid data"}), 400

    try:
        insert_data_from_json(data)
        return jsonify({"status": "Data received and saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


example = {
    "obstacle_data": [
        ["ObstacleLongCube", 800, 0],
        ["ObstacleTrain", 800, 2]
    ],
    "hit_obstacles": [
        ["ObstacleGate", "right", "light", 1700, None, 1700.043, 0.449, 2.0]
    ],
    "player_satisfaction": -1,
    "map_data": [
        ["SecondObstacleMap", 0.2, 0.3, 0.1, "COLOR_THEME_COLORFULL", 500, 2500, 250]
    ],
    "player_emotions": [
        [["neutral", 65.14600372314453], ["fear", 27.661518096923828], 1.0, 336.7202453613281],
    ],
    "score": 3094,
    "playing_time": 13.588539123535156,
    "difficulties": [1],
    "keys_pressed": [
        [
            "space",
            216.7677001953125
        ],
        [
            "space",
            870.7516479492188
        ]
    ]
}

if __name__ == '__main__':
    insert_data_from_json(example)
    # app.run(debug=True)

