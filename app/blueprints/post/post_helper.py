from . import post_db_helper as Post_DB
import db.db_error_helper as ERROR
from openai import OpenAI
import json
import os
from app.models.post import Post
from datetime import datetime
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user.user_helper import UserService

api_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=api_key)

user_helper = UserService()


def get_post(data):
    """Get post data by postid"""
    try:
        return Post_DB.get_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def add_post(data):
    """Add new post"""
    new_post = {
        'userid': data['userid'],
        'title': data.get('title', '(NO TITLE)'),
        'content': data.get('content', '(NO CONTENT)'),
        'posttime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'posttype': data.get('posttype', 'Murder Mystery'),
        'puzzleid': data.get('puzzleid', 1)
    }
    try:
        return Post_DB.add_post(Post, new_post)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))



def edit_post(data):
    """Edit post"""
    data['posttime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        return Post_DB.edit_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def delete_post(data):
    """Delete post"""
    try:
        return Post_DB.delete_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def get_post_full(postid):
    post = get_post({'postid': postid})
    # we don't want everyone to know the puzzle answer :P
    puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})['puzzledata']
    comment = []
    comments = comment_helper.get_comments({"postid": postid})
    if comments is not None:
        for item in comments:
            item['author'] = user_helper.get_username(item['userid'])
            item['avatarid'] = user_helper.get_avatarid(item['userid'])
            comment.append(item)
    return {"postid": post['postid'], "title": post['title'], "content": post['content'],
            "puzzledata": puzzledata, "comments": comment, "postimage": post['postimage']}


def generate_story(title, content, characters):
    prompt = f"""
            Title: {title}
            Content: {content}
            Characters: {characters}

            Generate a murder mystery story and identify the killer with an explanation.
            DO NOT REVEAL THE KILLER IN THE STORY
            Reply in JSON with the format:
            {{
                "story": "<story_text>",
                "killer": "<killer_name>",
                "explanation": "<explanation>"
            }}
            """

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a creative assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300)

        story = response.choices[0].message.content.strip()
        story_data = json.loads(story)
        return story_data
    except Exception as e:
        print(e)
        return "An error occurred while generating the story."
def add_image(data):
    try:
        return Post_DB.add_image(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
