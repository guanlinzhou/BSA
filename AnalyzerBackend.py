import sys
import praw
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions, ConceptsOptions, EntitiesOptions

def get_text_samples(subname, n_posts, n_comments_per_post):
    """Extract text samples from reddit."""
    reddit = praw.Reddit(client_id='3VF3aqQ8Lr1Ceg', client_secret='sfpMy2z4YYGoiuWHAkPrOlZgj04', password='bRAggER95$',user_agent='Post_Extraction',username='Baker_Street_Analyt')
    subreddit = reddit.subreddit(subname)
    samples = []
    print('Format: Title | Score')
    print('________________________________________________')  
    for submission in subreddit.hot(limit=n_posts):
        if submission.title:
            print(submission.title,'|',submission.score)
            samples.append(submission.title)
        if submission.selftext:
            # (selftext can be empty)
            samples.append(submission.selftext)
        submission.comments.replace_more(limit=0) # get rid of "More comments..." placeholders
        submission.comment_sort = 'top'
        i = 1 # counting how many comments we've processed
        for comment in submission.comments:
            if comment.body:
                samples.append(comment.body)
                i += 1
            if i > n_comments_per_post:
                break
    print('________________________________________________')    
    return samples
    #return ['\n\n'.join(samples)]
'''progress updates to make it more seeable'''
def get_nlu_data(samples):
    """Query IBM NLU to get keyword data for each sample."""
    data = {}
    nlu = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        username='764f1427-efb8-41b7-96b5-ab585021e5da',
        password='GwnlOQ77YmGy')
    for s in samples:
        response = nlu.analyze(
            text=s,
            language='en',
            features=Features(
                keywords=KeywordsOptions(
                    emotion=True,
                    limit=5),
                entities=EntitiesOptions(
                    emotion=True,
                    limit=5)
            ))
        data[s] = {'key' : {}, 'ent' : {}}
        for kwd_data in response.result['keywords']:
            if ('relevance' not in kwd_data or 'emotion' not in kwd_data):
                continue # skip this one, it doesn't have full data?
            data[s]['key'][kwd_data['text']] = kwd_data
        for ent_data in response.result['entities']:
            if ('relevance' not in ent_data or 'emotion' not in ent_data):
                continue #yuh yeet
            data[s]['ent'][ent_data['text']] = ent_data
    return data
  
def get_common_words(nlu_data, n, ty):
    """Get the top n keywords."""
    relevance = {}
    for sample in nlu_data:
        for keyword in nlu_data[sample][ty]:
            if keyword not in relevance:
                relevance[keyword] = 0
            relevance[keyword] += nlu_data[sample][ty][keyword]['relevance']
    return sorted(list(relevance.keys()), key=lambda k: relevance[k], reverse=True)[:n]

def get_emotion_information(nlu_data, keywords, ty):
    emotion = {} # keyword -> [happy factor, unhappy factor]
    for kw in keywords:
        emotion[kw] = [0.0, 0.0]
        count = 0 # number of samples incorporated
        for sample in nlu_data:
            if kw not in nlu_data[sample][ty]:
                continue
            count += 1
            emotion[kw][0] += nlu_data[sample][ty][kw]['emotion']['joy']*4.0 # there are 4 sad factors and only one happy one
            emotion[kw][1] += sum([nlu_data[sample][ty][kw]['emotion'][a] for a in ['sadness', 'fear', 'disgust', 'anger']])
        # perform averaging
        emotion[kw][0] = emotion[kw][0]/count
        emotion[kw][1] = emotion[kw][1]/count
    return emotion

def graph_app(common, emotions):
    app = dash.Dash()
    happy, sad, mood = [], [], []
    for x in common:
        mood.append([-emotions[x][1], emotions[x][0]])
        happy.append(emotions[x][0])
        sad.append(-emotions[x][1])
    x = [y for y in range(len(happy))]
    app.layout = html.Div(children=[
        html.H1(children='DeepAnalyzer'),

        html.Div(children='''
            A Deep Analyzer of subreddit trends
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    #{'x': x, 'y': mood, 'type': 'bar', 'name': 'Mood'},
                    {'x': common, 'y': happy, 'type': 'bar', 'name': 'Happy'},
                    {'x': common, 'y': sad, 'type': 'bar', 'name': 'Sad'},
                ],
                'layout': {
                    'title': 'Keyword Analysis',
                    'barmode':'relative',
                }
            }
        )
    ])
    app.run_server(debug=True)



def main():
    SUBREDDIT = sys.argv[1]
    N_POSTS = int(sys.argv[2])
    N_COMMENTS_PER_POST = int(sys.argv[3])
    N_KEYWORDS_WANTED = int(sys.argv[4])
    samples = get_text_samples(SUBREDDIT, N_POSTS, N_COMMENTS_PER_POST)
    data = get_nlu_data(samples)
    
    
    
    """
    sys.stdout.write('keyword\thappy_score\tunhappy_score\n')
    for keyword in common:
        sys.stdout.write('{}\t{}\t{}\n'.format(keyword, emotions[keyword][0], emotions[keyword][1]))
    """
    graph_app(common, emotions)
    
if __name__ == '__main__':
    main()

#some sort of print function that displays wtf is happening LUL

#go back to the json created by the first subfunction; then identify strings with the keywords generated, then produce a sentiment reading for the selected posts
#output in conjunction with upvote values

#after this take the data that's been printed then use libmatplot in order to produce some d o p e graphics for the advertising reps

'''Traceback (most recent call last):
  File "c:/Users/Siddu/Documents/CompBioProjects/hackMIT/penultimate_reddit_analyzer.py", line 87, in <module>
    main()
  File "c:/Users/Siddu/Documents/CompBioProjects/hackMIT/penultimate_reddit_analyzer.py", line 79, in main
    keyword_data = get_nlu_keyword_data(samples)
  File "c:/Users/Siddu/Documents/CompBioProjects/hackMIT/penultimate_reddit_analyzer.py", line 43, in get_nlu_keyword_data
    for kwd_data in response['keywords']:
TypeError: 'DetailedResponse' object is not subscriptable'''
