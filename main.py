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

        s = StudentS(username=username, id=(number+1))
        key = s.put()
        temp1 = """
		<p>Current length of students' list: {{number}}, 1st query: {{query}}, key added: {{key}}</p>
		"""
        ret = template(temp1, number=number, query=query, key=key)
        return ret
        # temp1="""
        # 	'''<h1> </h1>
        # 	<head>
        # 	<style>
        # 	.wrapper {text-align: center;}
        # 	</style>
        # 	</head>
        # 	<div class="wrapper">
        # 		<h3>Welcome {{username}} </h3>
        # 		<p> Your ID is (not implemented yet). You can see the available rooms in the button below.
        # 		<input type="button" value="See available rooms" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/student/{{student_id}}';" />
        # 		<p>Under construction...</p>
        # 	</div>'''
        # """

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
            <h1>CAMPUS</h1>
            %for r in rooms:
                <p>
                <a href="https://1-dot-asint-151811.appspot.com/init/student/listrooms/{{student_id}}/{{r.id}}"> {{r.name}} </a>
                </p>
            % end
            <input type="button" value="Back" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/';" />
            """


      # for r in rooms:
       #     ret += "      " + r.name + "       " + r.id + "<br>"
    else:
        ret = """
            <p>ID not found! </p>
        """

    return template(ret, rooms=rooms, student_id=student_id)

@bottle.route('/init/student/<student_id>/<room_id>')
def list_rooms(student_id, room_id):
    students = StudentS.query(StudentS.room_id==int(room_id)).fetch()
    room_name = "coisa qq"
    q_current_room = RoomR.query(RoomR.id == str(room_id)).fetch()
    for r in q_current_room:
        room_name = r.name

    ret = """
        <head>
		<style>
		.wrapper {text-align: center;}
		</style>
		</head>
        <div class="wrapper">
			<h3>List of students in room {{room_name}}</h3>
			%for s in students:
                <p>{{s.name}}</p>
            % end
			<button id="b_checkin" onclick="CheckIn()">Check In</button>
			<button id="b_checkout" onclick="CheckOut()">Check Out</button>
            <input type="button" value="Back" onclick="window.history.back()" />
            <p id="added">cOcO</p>
        </div>

        <script>
            function CheckIn() {
                alert("Button Check Out");

                document.getElementById("added").innerHTML = "Added1!"
                var xhttp = new XMLHttpRequest();
                document.getElementById("added").innerHTML = "Added2!"
                xhttp.open("POST", "/init/student/{{student_id}}/{{room_id}}/in", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send(JSON.stringify({'cmd':'IN'}));
                document.getElementById("added").innerHTML = "Checked in!"

                document.getElementsById("b_checkin").style.visibility="hidden";
                document.getElementsById("b_checkout").style.visibility="visible";
            }

            function CheckOut() {
                alert("Button Check Out");

                document.getElementById("added").innerHTML = "Added1!"
                var xhttp = new XMLHttpRequest();
                document.getElementById("added").innerHTML = "Added2!"
                xhttp.open("POST", "/init/student/{{student_id}}/{{room_id}}/out", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send(JSON.stringify({'cmd':'OUT'}));
                document.getElementById("added").innerHTML = "Checked out!"

                document.getElementsById("b_checkout").style.visibility="hidden";
                document.getElementsById("b_checkin").style.visibility="visible";
            }
        </script>
                """
    return template(ret, student_id=student_id, room_id=room_id, students=students, room_name=room_name)

@bottle.post('/init/student/<student_id>/<room_id>/<in_or_out>')
def check_in_or_out(student_id, room_id, in_or_out):
    st_list = StudentS.query(StudentS.room_id == int(room_id)).fetch()

    for s in st_list:
        s_key = s.key()
    student = StudentS.get(s_key)
    student.room_id = room_id
    student.put()


@bottle.route('/init/admin/')
def admin():
    response = urllib2.urlopen(
        'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces')  # Request list of campus using Tecnico API
    infoFromJson = json.loads(response.read())
    print infoFromJson
    # Display retrieved list of Campus in an HTML page. Each

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
            <input type="button" value="Back" onclick="window.history.back()" />
            <input type="button" onclick="location.href='https://1-dot-asint-151811.appspot.com/init/admin/';" value="Go to Admin Homepage" />
            <p id="added">cOcO</p>
        </div>

        <script>
            function add_room(){
                document.getElementById("added").innerHTML = "Added1!"
                var xhttp = new XMLHttpRequest();
                document.getElementById("added").innerHTML = "Added2!"
                xhttp.open("POST", "/init/admin/search/addroom", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send(JSON.stringify({'id':'{{json["id"]}}' ,'name':'{{json["name"]}}'}));
                document.getElementById("added").innerHTML = "Added!"
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
