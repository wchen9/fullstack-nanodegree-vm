from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return
            if self.path.endswith("/edit"):
                rid = self.path.split('/')[2]
                session = DBSession()
                rows = session.query(Restaurant).filter_by(id = rid).one()
                if rows != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += '''<form method='POST' enctype='multipart/form-data' action=%s>
                             <h2>Edit Restaurant Name</h2>
                             <input name="message" type="text" placeholder = '%s'>
                             <input type="submit" value="Submit"> </form>''' % (self.path, rows.name)
                    output += "</body></html>"
                    self.wfile.write(output)
                return
            if self.path.endswith("/delete"):
                rid = self.path.split('/')[2]
                session = DBSession()
                row = session.query(Restaurant).filter_by(id = rid).one()
                if row != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += '''<form method='POST' enctype='multipart/form-data' action=%s>
                             <h2>Are You Sure You Want To Delete Restaurant %s</h2>
                             <input type="submit" value="Submit"> </form>''' % (self.path, row.name)
                    output += "</body></html>"
                    self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                session = DBSession()
                rows = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create New Restaurant</a></br></br>"
                for row in rows:
                    output += "%s</br>" % row.name
                    output += '<a href = "/restaurants/%d/edit">Edit</a></br>' % row.id
                    output += '<a href = "/restaurants/%d/delete">Delete</a></br>' % row.id
                    output += '</br>'
                output += "</body></html>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                             <h2>Create new restaurant</h2>
                             <input name="message" type="text" >
                             <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                rid = self.path.split('/')[2]
                session = DBSession()
                rows = session.query(Restaurant).filter_by(id = rid).one()
                if rows != []:
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    #print(self.headers)
                    ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        session.delete(rows)
                        session.commit()
                return
            if self.path.endswith("/edit"):
                rid = self.path.split('/')[2]
                session = DBSession()
                rows = session.query(Restaurant).filter_by(id = rid).one()
                if rows != []:
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('message')
                        rows.name = messagecontent[0]
                        session.add(rows)
                        session.commit()
                return

            if self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session = DBSession()
                    session.add(newRestaurant)
                    session.commit()
                output = ""
                output += "<html><body>"
                output += "<h2> Created restaurant %s </h2>" % messagecontent[0]
                output += "<a href = '/restaurants'>Back to Restaurant List</a>"
                output += "</body></html>"
                self.wfile.write(output)
                return
           
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()