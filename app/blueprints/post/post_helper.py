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
import app.blueprints.leaderboard.siteleaderboard_helper as Slb_Helper

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key="hi")

user_helper = UserService()


def clean_control_characters(text):
    return ''.join(c for c in text if c.isprintable())


def get_post(data):
    """Get post data by postid"""
    try:
        return Post_DB.get_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def get_all_posts_with_comments(start_index=0, limit=10):
    """Get all posts with their comments and additional details, with pagination"""
    try:
        all_posts = Post_DB.get_all_posts(Post)

        paginated_posts = all_posts[start_index:start_index + limit]

        full_posts = []

        for post in paginated_posts:
            # Fetch additional post details
            postid = post['postid']
            puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})['puzzledata']
            comments = []
            post_comments = comment_helper.get_comments({"postid": postid})

            if post_comments is not None:
                for item in post_comments:
                    item['author'] = user_helper.get_username(item['userid'])
                    item['avatarid'] = user_helper.get_avatarid(item['userid'])
                    comments.append(item)

            full_post = {
                "postid": post['postid'],
                "title": post['title'],
                "content": post['content'],
                "puzzledata": puzzledata,
                "comments": comments,
                "postimage": post.get('postimage')
            }
            full_posts.append(full_post)

        return full_posts

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
        Slb_Helper.new_post(data['userid'])
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


def generate_story(title, content, characters, answer):
    #             Generate a murder mystery story and identify the killer with an explanation.
    #             YOU MUST USE ONE OF THE CHARACTERS PROVIDED AS THE KILLER.
    #             DO NOT REVEAL THE KILLER IN THE STORY.
    #             Reply in JSON with the format:
    #             {{
    #                 "story": "<story_text>",
    #                 "killer": "<killer_name>",
    #                 "explanation": "<explanation>"
    #             }}

    prompt = f"""
            Title: {title}
            Content: {content}
            Characters: {characters}
            Answer: {answer}
            
            Create an engaging and detailed murder mystery game playable script for players to guess the killer. 
            The story should be long enough to provide a rich, immersive experience.
            After the story, include a series of clues that allow players to deduce one of the provided characters as the killer.
            Think carefully of these clues, as players will need space to think, they can be somehow misleaded to make the puzzle more interesting to play,
            but these clues still need to be coherent, sensible, and logically correct as crucial part of "playable game script".
            DO NOT reveal the answer(killer) AT ANY FORM.
            Ensure the killer is one of the listed characters.

            Limit your whole output to 600 words.
            No need to include Title in your output.
            
            Reply in plaintext.
            """

    try:
        # response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
        response = client.chat.completions.create(model="gpt-4o-2024-05-13",

                                                  messages=[
                                                      {"role": "system", "content": "You are a creative assistant."},
                                                      {"role": "user", "content": prompt}
                                                  ],
                                                  max_tokens=1000)

        story = response.choices[0].message.content.strip()
        # raise RuntimeError(f"{story}")
        return story
    except Exception as e:
        print(e)
        raise RuntimeError(f"An error occurred while generating the story.{e}")


def add_image(data):
    try:
        return Post_DB.add_image(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
