from bottle import route, run, template, request, static_file
import plotly
from AnalyzerBackend import *

def plotly_experiment(common, emotions, outpath):
    happy, sad = [], []
    for x in common:
        happy.append(emotions[x][0])
        sad.append(-emotions[x][1])


    trace1 = {
        'x': common,
        'y': happy,
        'name': 'Happy',
        'type': 'bar'
    }
    trace2 = {
        'x': common,
        'y': sad,
        'name': 'Unhappy',
        'type': 'bar'
    }

    data = [trace1, trace2];
    layout = {
        'xaxis': {'title': 'X axis'},
        'yaxis': {'title': 'Y axis'},
        'barmode': 'relative',
        'title': 'Keyword Analysis'
    }
    plotly.offline.plot({'data': data, 'layout': layout}, filename=outpath, auto_open=False)

#Must have the Analyzer file in the same folder, run then go to http://localhost:8080/  

@route('/')
def main_site():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="/static/logic.js"></script>
    </head>
    <body>
    <div id="gradient">
        <div>  
        <center><h3>IBM Watson Reddit Keyword Analyzer</h3>  
        
            
              Subreddit: <br>
              <input name="subreddit" type="text" id="subreddit" placeholder="i.e. 'mechanicalkeyboards'..." /> <br>
              Posts: <br>
              <input name="posts" type="text" id="posts" placeholder="# of 'hot' posts to analyze..." /> <br>
              Comments: <br> 
              <input name="comments" type="text" id="comments" placeholder="# of comments per post..." /> <br>
              Keywords: <br>  
              <input name="keywords" type="text" id="keywords" placeholder="# of keywords to produce/analyze..." /> <br> <br>
            
              <input value="Submit For Analysis" type="submit" id="submit" />
               
          </div><br />
          <div class="loader" id="wheel"></div>
        <div id="results_outer">
        <div id="results_switcher_container">
            <div id="results_switcher_keywords">Keywords</div>
          <div id="results_switcher_entities">Entities</div></div>
        
        <div id="graph_keywords"></div>
        <div id="graph_entities"></div>
        
        </div>
    </div>
    </body></center>
    </html>
    '''

@route('/analyze', method='POST')
def do_analysis():
    subreddit = request.forms.get('subreddit')
    posts = int(request.forms.get('posts'))
    comments = int(request.forms.get('comments'))
    keywords = int(request.forms.get('keywords'))

    samples = get_text_samples(subreddit, posts, comments)
    data = get_nlu_data(samples)
    
    keyword_common = get_common_words(data, keywords, 'key')
    keyword_emotions = get_emotion_information(data, keyword_common, 'key')
    
    entity_common = get_common_words(data, keywords, 'ent')
    entity_emotions = get_emotion_information(data, entity_common, 'ent')
    
    plotly_experiment(keyword_common, keyword_emotions, 'gkeywords.html')
    plotly_experiment(entity_common, entity_emotions, 'gentities.html')
    
    return 'Success'
    """
   html =
<table>
    <tr>
    <th>Keyword</th>
    <th>Positive Emotion Score</th>
    <th>Negative Emotion Score</th>
  </tr>"""
    for kw in common:
      html += """
  <tr>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
  </tr>.format(kw, emotions[kw][0], emotions[kw][1])
    html += '</table>'
    return html"""
    
    #return "<p></p>"
        # if check_login(s, password):
        #     return "<p>Your login information was correct.</p>"
        # else:
        #     return "<p>Login failed. 
  
@route('/static/<filename:path>')
def serve_static(filename):
  return static_file(filename, root='./')

run(host='localhost', port=8080)
