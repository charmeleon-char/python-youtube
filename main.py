import jinja2
import os
import urllib
import webapp2
import json

from apiclient.discovery import build

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

REGISTRATION_INSTRUCTIONS = """
    You must set up a project and get an API key to run this code. <br> 
    Steps: <br>
    1.  Visit <a href="https://developers.google.com/youtube/v3/code_samples/python_appengine#create-api-key"
    target='_top'>https://developers.google.com/youtube/v3/code_samples/python_appengine#create-api-key</a> 
    for instructions on setting up a project and key. Make sure that you have 
    enabled the YouTube Data API (v3) for your project. 
    You do not need to set up OAuth credentials for this project. <br>
    2.  Once you have obtained a key, search for the text 'REPLACE_ME' in the 
    code and replace that string with your key. <br> 
    3.  Click the reload button above the output container to view the new output. """

# Set API_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API and Freebase API
# for your project.
API_KEY = "AIzaSyAPXQhLIYiBfIbHNha8ocjzziZD-V0nkOU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
QUERY_TERM = "LaureateChannel"

class whynot(webapp2.RequestHandler):
    def get(self):
        self.search_by_keyword()

    def search_by_keyword(self):
       youtube = build(
                 YOUTUBE_API_SERVICE_NAME, 
                 YOUTUBE_API_VERSION, 
                 developerKey=API_KEY
        )
       channels_response = youtube.channels().list(
          forUsername=QUERY_TERM,
          part='snippet,contentDetails'
       ).execute()

    # channels_response = youtube.channels().list(
     #     categoryId=self.request.get('descrip'),
     #     part='snippet,contentDetails'
     # ).execute()
       channel_name = ''
       videos = []
       for channel in channels_response['items']:
          uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']
          channel_name = channel['snippet']['title']
          
          next_page_token = ''
          while next_page_token is not None:
            playlistitems_response = youtube.playlistItems().list(
                playlistId=uploads_list_id,
                part='snippet',
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for playlist_item in playlistitems_response['items']:
              videos.append(playlist_item)
              
            next_page_token = playlistitems_response.get('tokenPagination', {}).get(
                'nextPageToken')
            
            if len(videos) > 100:
              break

       template_values = {
        'channel_name': channel_name,
        'videos': videos
        }
       self.response.headers.add_header("Access-Control-Allow-Origin", "*")
       self.response.headers['Content-type'] = 'application/json'
       self.response.out.write(json.dumps(template_values))
      

        #items = request.POST
        #r = Review(location=items['location'], description=items['review'], title=items['title'], star_rating=int(items['stars']))
        #r.date = datetime.datetime.now().date()
       

class Jsonhandler(webapp2.RequestHandler):
    def post(self):
        self.search_by_keyword()

    def search_by_keyword(self):
       youtube = build(
                 YOUTUBE_API_SERVICE_NAME, 
                 YOUTUBE_API_VERSION, 
                 developerKey=API_KEY
        )
       search_response = youtube.search().list(
           q= self.request.get('title'),
          part = 'id,snippet',
          maxResults=50
        ).execute()

       videos = []

       for search_result in search_response.get("items", []):
          videos.append(search_result)
       
       template_values = {
         'videos': videos
        }       
       self.response.headers.add_header("Access-Control-Allow-Origin", "*")
       self.response.headers['Content-type'] = 'application/json'
       self.response.out.write(json.dumps(template_values))
      

class testhandler(webapp2.RequestHandler):
  def get(self):
       self.response.headers['Content-type'] = 'text/html'
       self.response.write('hola es test ') 

class MainHandler(webapp2.RequestHandler):
  def get(self):
   
      self.search_by_keyword()

  def search_by_keyword(self):
    youtube = build(
      YOUTUBE_API_SERVICE_NAME, 
      YOUTUBE_API_VERSION, 
      developerKey=API_KEY
    )
    search_response = youtube.search().list(
     q=QUERY_TERM,
      part="id,snippet",
      maxResults=50
    ).execute()
    channel_name = ''
    videos = []
    for channel in channels_response['items']:
       uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']
       channel_name = channel['snippet']['title']
      
    next_page_token = ''
    while next_page_token is not None:
        playlistitems_response = youtube.playlistItems().list(
              playlistId=uploads_list_id,
              part='snippet',
              maxResults=50,
              pageToken=next_page_token
        ).execute()
        
        for playlist_item in playlistitems_response['items']:
              videos.append(playlist_item)
              
        if len(videos) > 100:
          break
    template_values = {
      'channel_name': channel_name,
      'videos': videos
    }

    self.response.headers['Content-type'] = 'text/html'
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

class potatohanlder(object):
  def get(self):
        self.response.headers['Content-type'] = 'text/html'
        self.response.write('hola desde los json ')        

class routehandler(object):
  def get(self):
      self.response.headers['Content-type'] = 'text/html'
      self.response.write('usando mal el render ')        



app = webapp2.WSGIApplication([
  ('/*', routehandler),
   ('/json/', Jsonhandler),
   ('/try/', whynot),
   ('/potato/',potatohanlder)
 
], debug=True)



