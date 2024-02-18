import flask
from flask import session, render_template, Flask, redirect, request, url_for
from flask_socketio import send, join_room, leave_room, SocketIO,emit
import pickle
import base64
import json
from string import ascii_uppercase
import numpy as np
from PIL import Image
import re
import io
import tensorflow as tf
import cv2
import random


labels = ['aircraft carrier',
 'airplane',
 'alarm clock',
 'ambulance',
 'angel',
 'animal migration',
 'ant',
 'anvil',
 'apple',
 'arm',
 'asparagus',
 'axe',
 'backpack',
 'banana',
 'bandage',
 'barn',
 'baseball bat',
 'baseball',
 'basket',
 'basketball',
 'bat',
 'bathtub',
 'beach',
 'bear',
 'beard',
 'bed',
 'bee',
 'belt',
 'bench',
 'bicycle',
 'binoculars',
 'bird',
 'birthday cake',
 'blackberry',
 'blueberry',
 'book',
 'boomerang',
 'bottlecap',
 'bowtie',
 'bracelet',
 'brain',
 'bread',
 'bridge',
 'broccoli',
 'broom',
 'bucket',
 'bulldozer',
 'bus',
 'bush',
 'butterfly',
 'cactus',
 'cake',
 'calculator',
 'calendar',
 'camel',
 'camera',
 'camouflage',
 'campfire',
 'candle',
 'cannon',
 'canoe',
 'car',
 'carrot',
 'castle',
 'cat',
 'ceiling fan',
 'cell phone',
 'cello',
 'chair',
 'chandelier',
 'church',
 'circle',
 'clarinet',
 'clock',
 'cloud',
 'coffee cup',
 'compass',
 'computer',
 'cookie',
 'cooler',
 'couch',
 'cow',
 'crab',
 'crayon',
 'crocodile',
 'crown',
 'cruise ship',
 'cup',
 'diamond',
 'dishwasher',
 'diving board',
 'dog',
 'dolphin',
 'donut',
 'door',
 'dragon',
 'dresser',
 'drill',
 'drums',
 'duck',
 'dumbbell',
 'ear',
 'elbow',
 'elephant',
 'envelope',
 'eraser',
 'eye',
 'eyeglasses',
 'face',
 'fan',
 'feather',
 'fence',
 'finger',
 'fire hydrant',
 'fireplace',
 'firetruck',
 'fish',
 'flamingo',
 'flashlight',
 'flip flops',
 'floor lamp',
 'flower',
 'flying saucer',
 'foot',
 'fork',
 'frog',
 'frying pan',
 'garden hose',
 'garden',
 'giraffe',
 'goatee',
 'golf club',
 'grapes',
 'grass',
 'guitar',
 'hamburger',
 'hammer',
 'hand',
 'harp',
 'hat',
 'headphones',
 'hedgehog',
 'helicopter',
 'helmet',
 'hexagon',
 'hockey puck',
 'hockey stick',
 'horse',
 'hospital',
 'hot air balloon',
 'hot dog',
 'hot tub',
 'hourglass',
 'house plant',
 'house',
 'hurricane',
 'ice cream',
 'jacket',
 'jail',
 'kangaroo',
 'key',
 'keyboard',
 'knee',
 'knife',
 'ladder',
 'lantern',
 'laptop',
 'leaf',
 'leg',
 'light bulb',
 'lighter',
 'lighthouse',
 'lightning',
 'line',
 'lion',
 'lipstick',
 'lobster',
 'lollipop',
 'mailbox',
 'map',
 'marker',
 'matches',
 'megaphone',
 'mermaid',
 'microphone',
 'microwave',
 'monkey',
 'moon',
 'mosquito',
 'motorbike',
 'mountain',
 'mouse',
 'moustache',
 'mouth',
 'mug',
 'mushroom',
 'nail',
 'necklace',
 'nose',
 'ocean',
 'octagon',
 'octopus',
 'onion',
 'oven',
 'owl',
 'paint can',
 'paintbrush',
 'palm tree',
 'panda',
 'pants',
 'paper clip',
 'parachute',
 'parrot',
 'passport',
 'peanut',
 'pear',
 'peas',
 'pencil',
 'penguin',
 'piano',
 'pickup truck',
 'picture frame',
 'pig',
 'pillow',
 'pineapple',
 'pizza',
 'pliers',
 'police car',
 'pond',
 'pool',
 'popsicle',
 'postcard',
 'potato',
 'power outlet',
 'purse',
 'rabbit',
 'raccoon',
 'radio',
 'rain',
 'rainbow',
 'rake',
 'remote control',
 'rhinoceros',
 'rifle',
 'river',
 'roller coaster',
 'rollerskates',
 'sailboat',
 'sandwich',
 'saw',
 'saxophone',
 'school bus',
 'scissors',
 'scorpion',
 'screwdriver',
 'sea turtle',
 'see saw',
 'shark',
 'sheep',
 'shoe',
 'shorts',
 'shovel',
 'sink',
 'skateboard',
 'skull',
 'skyscraper',
 'sleeping bag',
 'smiley face',
 'snail',
 'snake',
 'snorkel',
 'snowflake',
 'snowman',
 'soccer ball',
 'sock',
 'speedboat',
 'spider',
 'spoon',
 'spreadsheet',
 'square',
 'squiggle',
 'squirrel',
 'stairs',
 'star',
 'steak',
 'stereo',
 'stethoscope',
 'stitches',
 'stop sign',
 'stove',
 'strawberry',
 'streetlight',
 'string bean',
 'submarine',
 'suitcase',
 'sun',
 'swan',
 'sweater',
 'swing set',
 'sword',
 'syringe',
 't-shirt',
 'table',
 'teapot',
 'teddy-bear',
 'telephone',
 'television',
 'tennis racquet',
 'tent',
 'The Eiffel Tower',
 'The Great Wall of China',
 'The Mona Lisa',
 'tiger',
 'toaster',
 'toe',
 'toilet',
 'tooth',
 'toothbrush',
 'toothpaste',
 'tornado',
 'tractor',
 'traffic light',
 'train',
 'tree',
 'triangle',
 'trombone',
 'truck',
 'trumpet',
 'umbrella',
 'underwear',
 'van',
 'vase',
 'violin',
 'washing machine',
 'watermelon',
 'waterslide',
 'whale',
 'wheel',
 'windmill',
 'wine bottle',
 'wine glass',
 'wristwatch',
 'yoga',
 'zebra',
 'zigzag']


def generatecode(length):
	code = ""
	while True:
		for i in range(length):
			code += random.choice(ascii_uppercase)
		if code not in rooms:
			break
	return code


model = tf.keras.models.load_model('quickdraw64.h5', compile=False)


# Initialize the useless part of the base64 encoded image.
init_Base64 = 21


# Initializing new Flask instance. Find the html template in "templates".
app = Flask(__name__)
app.config["SECRET_KEY"] = "Omalve"
socketio = SocketIO(app)
idx = 0
# Initialize the useless part of the base64 encoded image.
init_Base64 = 21

# Rooms dictionary to keep track of users in each room
rooms = {}


@app.route("/", methods=["GET", "POST"])
def home():
	session.clear()
	if request.method == "POST":
		name = request.form.get("name")
		code = request.form.get("code")
		join = request.form.get("join", False)
		create = request.form.get("create", False)

		if not name:
			return render_template("home.html", error="Please enter a name.", code=code, name=name)

		if join != False and not code:
			return render_template("home.html", error="Please enter a room code.", code=code, name=name)

		room = code
		if create != False:
			room = generatecode(4)
			rooms[room] = {"members": {}, "object": labels[random.choice(range(0, len(labels)))]}
		elif code not in rooms:
			return render_template("home.html", error="Room does not exist.", code=code, name=name)

		session["room"] = room
		session["name"] = name
		session["score"] = 0
		return redirect(url_for("room"))

	return render_template("home.html")


@app.route("/draw", methods=["GET", "POST"])
def room():
	room = session.get("room")
	if room is None or session.get("name") is None or room not in rooms:
		return redirect(url_for("home"))
	return render_template("draw.html", code=room, object=rooms[room]["object"])

	



@socketio.on("canvas_data")
def get_canvas_data(data):
	name = session.get('name')
	room = session.get('room')
	# Process the canvas data here
	draw = data
	draw = draw[init_Base64:]
	draw_decoded = base64.b64decode(draw)
	image = np.asarray(bytearray(draw_decoded), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
	resized = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)
	vect = np.asarray(resized, dtype="uint8")
	img = vect.reshape(1, 64, 64, 1).astype('float32')
	out = model.predict(img)
	object_index = labels.index(rooms[room]['object'])
	score = out[0][object_index]
	scale_value = lambda value: value * 10
	score = scale_value(score)

	rooms[room]["members"][name] += float(score)
	members = rooms[room]["members"]
	member_list = [{"name": k, "score": v} for k, v in members.items()]
	socketio.emit("members_update", member_list, room=room)

	


@socketio.on("connect")
def connect():
	room = session.get("room")
	name = session.get("name")
	score = session.get("score")
	if not room or not name:
		return
	if room not in rooms:
		rooms[room] = {"members": {}, "object": labels[random.choice(range(0, len(labels)))]}
	join_room(room)
	rooms[room]["members"][name] = score

	# Send the list of members and their scores as a message
	members = rooms[room]["members"]
	member_list = [{"name": k, "score": v} for k, v in members.items()]
	socketio.emit("members_update", member_list, room=room)

	print(f"{name} has joined the room {room}")


@socketio.on("disconnect")
def disconnect():
	room = session.get("room")
	name = session.get("name")
	score = session.get("score")
	leave_room(room)

	if room in rooms:
		rooms[room]["members"].pop(name)
		members = rooms[room]["members"]
		member_list = [{"name": k, "score": v} for k, v in members.items()]
		socketio.emit("members_update", member_list, room=room)
		if len(rooms[room]["members"]) == 0:
			del rooms[room]

	print(f"{name} has left the room {room}")


if __name__ == '__main__':
	socketio.run(app, debug=True)
