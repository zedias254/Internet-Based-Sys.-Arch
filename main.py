"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle, debug, template, request, post, get
import json
import urllib2
from google.appengine.ext import ndb

debug(True)
# Create the Bottle WSGI application.
bottle = Bottle()

class MessageM(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class StudentS(ndb.Model):
    username = ndb.StringProperty()
    id = ndb.IntegerProperty()
    room_id = ndb.IntegerProperty()
class RoomR(ndb.Model):
    name = ndb.StringProperty()
    id =  ndb.StringProperty()

# students = ndb.StructuredProperty(, repeated=True)


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@bottle.route('/init/')
def init():
    temp1 = """
   		 <h1> </h1>
		<head>
		<style>
		.wrapper {text-align: center;}
		</style>
		</head>
		<div class="wrapper">
			<img src="http://users.isr.ist.utl.pt/~jmessias/content/img/IST_A_RGB_POS.jpg" alt="LogoIST" style="width:105px;height:41px;">
			<h2>Project for Internet Based Systems Architecture<h2/>
			<h3>Developed by: Ricardo S. Miranda [75757] & Jose M.Dias [75847] </h3>
			<p class="main1">An administrator can add rooms for students to occupy and check their occupancy.</p>
			<p class="main2">A student can occupy any of the available rooms by checking in and checking out when leaving.</p>
			<p> </p>
			<p class="main3"> You are:
			<input class="button" type="button" value="Administrator" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';" />
			<input class="button"type="button" value="Student" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/student/register/';" />
        	</p>
        </div>

    """
    # print json2html.convert(json=infoFromJson)
    return template(temp1)

@bottle.get('/init/student/register/')
def student():
    temp1 = """
		<h1> </h1>
		<head>
		<style>
		.wrapper {text-align: center;}
		</style>
		</head>
		<div class="wrapper">
			<h3>First, enter your username:</h3>
			<form action="/init/student/register/" method="post">
				Name: <input type="text" name="username"><br>
				<button type="submit">Submit</button>

			</form>
			<p> </p>
			<button type="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/';">Back</button>
			<p>Under construction...</p>
		</div>
    """
    # print json2html.convert(json=infoFromJson)
    return template(temp1)

@bottle.post('/init/student/register/')
def register():
    username = request.forms.get('username')
    query = StudentS.query(StudentS.username == username).count()
    if query:
        temp1 = """
			  <p>Username {{username}} already exists! Query: {{query}}</p>
			  """
        ret = template(temp1, username=username, query=query)
        return ret
    else:
        number = StudentS.query().count()
        #students = StudentS.query()
        #s_len = students.fetch()

        new_id = number+1
        s = StudentS(username=username, id=new_id)
        key = s.put()


        temp1="""
        	<h1> </h1>
        	<head>
        	<style>
        	.wrapper {text-align: center;}
        	</style>
        	</head>
        	<div class="wrapper">
        		<h3>Welcome {{username}} </h3>
                <p>Your ID is {{new_id}}. You can see the available rooms in the button below.
        		<button onclick="location.href='https://1-dot-asint-151811.appspot.com/init/student/{{new_id}}';"> See available rooms</button>
        		<p>Under construction...</p>
        	</div>'''
        """

        # payload = {'name': 'value'}
        # r = requests.post(url, data=payload)
        # print "%s" %r


        # @bottle.route('/init/student/<name>')
        # def add(name):
        # print "XXXXXX"
        # m = MessageM(content = name)
        # key = m.put()
        # return " x"
        # return 'Message %s added with key %s' %(name, str(key.id()))
        ret = template(temp1, username=username,new_id=new_id)
        return ret

@bottle.route('/init/student/<student_id>')
def list_rooms(student_id):
    find_id = StudentS.query(StudentS.id==int(student_id)).count()
    if find_id:
        student = StudentS.query(StudentS.id==int(student_id)).fetch()
        for s in student:
            student_name = s.username
        ret = "You're logged as " + student_name
        rooms = RoomR.query().fetch()
        ret = """
            <h1> </h1>
            <head>
                <style>
                    .wrapper {
                        text-align: center;
                        width:1200px;
                        border-radius: 5px;
                        background-color: #f2f2f2;
                        padding: 20px;
                        display: table;
                        margin: 0 auto;

                    }
                    .wrapper2 {
                        text-align: center;
                        width:400px;
                        border-radius: 5px;
                        background-color: #e2e2e2;
                        padding: 20px;
                        display: table;
                        margin: 0 auto;
                    }
                    input[type=text] {
                        width: 60%;
                        padding: 12px 20px;
                        margin: 8px 0;
                        box-sizing: border-box;
                    }
                    input[type=button] {
                        width: 20%;
                        background-color: #4CAF50;
                        color: white;
                        padding: 14px 20px;
                        margin: 8px 0;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }

                    input[type=button]:hover {
                        background-color: #45a049;
                    }


                </style>
            </head>
            <div class="wrapper">
                <h3>List of available rooms:</h3>
                %for r in rooms:
                    <p>
                    <a href="https://1-dot-asint-151811.appspot.com/init/student/{{student_id}}/{{r.id}}"> {{r.name}} </a>
                    </p>
                % end
                <p></p>
                <button id="b_search_friend" onclick="Show_form()">Search a friend</button>
                <button onclick="location.href='https://1-dot-asint-151811.appspot.com/init/';">Back</button>
            </div>
            <div class="wrapper2" id="div_form">
                <script>document.getElementById('div_form').style.display = "none";</script>
                    <form id="form_friend">
                        Friends' Username: <input id="text_input" type="text" name="fusername"><br>
                        <p></p>
                    </form>
                    <input type="button" id="b_submit" value="Search" onclick="Search_friend()"/>
                    <p id="friend_room"></p>
                    <p id="debug"></p>
            </div>


            <script>
                function Show_form() {
                    document.getElementById('div_form').style.display = "table";
                    document.getElementById("b_search_friend").style.display = "none";
                }

                function Search_friend() {
                    var friend_username = document.getElementById("form_friend");
                    document.getElementById("debug").innerHTML = String(friend_username.elements[0].value);

                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.onreadystatechange = function() {
                        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                            var response_json = xmlHttp.responseText;
                            friend_room_name = JSON.parse(response_json);
                            if(friend_room_name["ErrorCode"] == "NOUSERFOUND"){
                                str = "Username provided does <b>not exist</b>";
                            } else if(friend_room_name["ErrorCode"] == "NULL"){
                                str = "Username provided is <b>not in a room</b>";
                            } else{
                                str = "Your friend is at <b>" + friend_room_name["Room"] + "</b>";
                            }
                            document.getElementById("friend_room").innerHTML = (str);
                        }

                    }
                    xmlHttp.open("GET", "https://1-dot-asint-151811.appspot.com/init/student/"+String(friend_username.elements[0].value)+"/room", true);
                    xmlHttp.send(null);

                }
            </script>
            """


      # for r in rooms:
       #     ret += "      " + r.name + "       " + r.id + "<br>"
    else:
        ret = """
            <p>ID not found! </p>
        """

    return template(ret, rooms=rooms, student_id=student_id)

@bottle.get('/init/student/<friend_username>/room')
def search_friend(friend_username):
    friend = StudentS.query(StudentS.username == friend_username).fetch(1)
    if not friend:
        ret = json.dumps({"ErrorCode": "NOUSERFOUND", "Room": ""}, sort_keys=True)
        #ret = "NOTFOUND"  # Friend does not exist
    else:
        if (friend[0].room_id is None):
            ret = json.dumps({"ErrorCode": "NULL", "Room": ""}, sort_keys=True)
            #ret = ""
        else:
            friend_room_name = RoomR.query(RoomR.id == str(friend[0].room_id).decode("utf-8")).fetch(1)[0].name
            ret = json.dumps({"ErrorCode": "", "Room": friend_room_name}, sort_keys=True)
            #ret = str(friend_room_name)
    return ret

@bottle.route('/init/student/<student_id>/<room_id>')
def list_rooms(student_id, room_id):
    students = StudentS.query(StudentS.room_id==int(room_id)).fetch()
    room_name = "coisa qq"
    q_current_room = RoomR.query(RoomR.id == str(room_id)).fetch(1)[0]
    room_name = q_current_room.name

    ret = """
        <head>
		<style>
		.wrapper {text-align: center;}
		</style>
		</head>
        <div class="wrapper">
			<h3>List of students in room {{room_name}}</h3>
			%for s in students:
                <li>{{s.username}}</li>
            % end
			<button id="b_checkin" onclick="CheckIn()">Check In</button>
			<button id="b_checkout" onclick="CheckOut()">Check Out</button>
            <input type="button" value="Back" onclick="window.history.back()" />
            <p id="check"></p>
        </div>

        <script>
            function CheckIn() {
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/init/student/{{student_id}}/{{room_id}}/in", true);
                xhttp.send();
                document.getElementById("check").innerHTML = "You have checked in!";
                document.getElementById("b_checkin").style.visibility="hidden";
                document.getElementById("b_checkout").style.visibility="visible";
            }

            function CheckOut() {
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/init/student/{{student_id}}/{{room_id}}/out", true);
                xhttp.send();
                document.getElementById("check").innerHTML = "You have checked out!";
                document.getElementById("b_checkout").style.visibility="hidden";
                document.getElementById("b_checkin").style.visibility="visible";
            }
        </script>
                """
    return template(ret, student_id=student_id, room_id=room_id, students=students, room_name=room_name)

@bottle.post('/init/student/<student_id>/<room_id>/<in_or_out>')
def check_in_or_out(student_id, room_id, in_or_out):
    student = StudentS.query(StudentS.id == int(student_id)).fetch(1)[0]
    if in_or_out == 'out':
        student.room_id = None
        student.put()
    elif in_or_out == 'in':
        student.room_id = int(room_id)
        student.put()
    return

@bottle.route('/init/admin/')
def admin():
    response = urllib2.urlopen(
        'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces')  # Request list of campus using Tecnico API
    infoFromJson = json.loads(response.read())
    print infoFromJson
    # Display retrieved list of Campus in an HTML page. Each
    temp1="""
    <h1>CAMPUS</h1>
    %for campus in json:
        <p>
        <a href="https://1-dot-asint-151811.appspot.com/init/admin/search/{{campus["id"]}}"> {{campus["name"]}} </a>
        </p>
    % end
    <input type="button" value="Back" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/';" />
    """
    # print json2html.convert(json=infoFromJson)
    return template(temp1, json=infoFromJson)

@bottle.get('/init/admin/search/<room_id>')
def search(room_id):
    print "Room ID: " + room_id
    response = urllib2.urlopen('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/' + room_id)
    response_json = json.loads(response.read())
    print response_json

    if not response_json["containedSpaces"]:
        temp = """
		<h1></h1>
		<head>
		<style>
		.wrapper {text-align: center;}
		</style>
		</head>
		<div class="wrapper">
            <h3>{{json["type"]}} - {{json["name"]}}</h3>
			<button onclick="add_room()">Add</button>
            <input type="button" value="Back" onclick="window.history.back()"/>
            <input type="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';" value="Go to Admin Homepage"/>
            <p id="check"></p>
        </div>

        <script>
            function add_room(){
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "/init/admin/search/addroom", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send(JSON.stringify({'id':'{{json["id"]}}' ,'name':'{{json["name"]}}'}));
                document.getElementById("check").innerHTML = "Added! Students can now occupy room <b>{{json["name"]}}</b>."
            }
        </script>
        """

    else:
        temp = """
        <h1>SELECT {{json["containedSpaces"][0]["type"]}} IN {{json["name"]}} {{json["type"]}}</h1>
        %for room in json["containedSpaces"]:
            <li>
            <a href="https://1-dot-asint-151811.appspot.com/init/admin/search/{{room["id"]}}">
            {{room["name"]}}
            </a>
            </li>
        % end
        <input type="button" value="Back" onclick="window.history.back()" />
        """

    return template(temp, json=response_json)

@bottle.post('/init/admin/search/addroom')
def add_room():
    data = request.json
    #response = urllib2.urlopen('https://1-dot-asint-151811.appspot.com/init/admin/search/<room_id>' + room_id)
    #response_json = json.loads(response.read())

    r = RoomR(name=data['name'], id=data['id'])
    key = r.put()
    temp1 = """
    		<p> JSON:{{data}},Name:{{data["name"]}}, ID:{{data["id"]}}</p>
    		"""
    ret = template(temp1, data=data)


    return ret

@bottle.route('/showall')
def showall():
    ret = ""
    msgs = MessageM.query()
    stds = StudentS.query()
    rooms = RoomR.query()
    for m in msgs:
        ret += str(m.key.id()) + "    " + m.content + "     " + str(m.date) + "<br>"
    for s in stds:
        ret += str(s.key.id()) + "    " + s.username + "<br>"
    for r in rooms:
        ret += str(r.key.id()) + "    " + r.name + "       " + r.id +"<br>"
    return ret

@bottle.route('/showsome/<start:int>/<end:int>')
def showsome(start, end):
    ret = ""
    msgs = MessageM.query()
    for m in msgs.fetch(offset=start, limit=end - start):
        ret += str(m.key.id()) + "    " + m.content + "     " + str(m.date) + "<br>"
    return ret

@bottle.route('/showexact/<string>')
def showexact(string):
    ret = ""
    msgs = MessageM.query(Message.content == string)
    for m in msgs:
        ret += str(m.key.id()) + "    " + m.content + "     " + str(m.date) + "<br>"
    return ret


# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
