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

api_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=api_key)

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
            
    Construct an engaging and detailed murder mystery game script. The narrative should unfold in a manner that immerses players and prompts them to guess the killer among the listed characters. Do not reveal the killer directly or indirectly at any point.
    
    The story should:
    - Be crafted with a clear beginning, middle, and an intriguing end.
    - Include distinct and memorable interactions between characters to develop suspicion and intrigue.
    - Provide a series of subtle clues and red herrings that integrate seamlessly into the story, allowing players to formulate theories about the killer's identity.
    - Exclude the character listed in 'answer' from being the victim.
    - Ensure that the narrative and clues are coherent, sensible, and maintain logical integrity to support a playable game script.
    
    The final part of the script should allow room for deduction without explicitly solving the mystery, thus enhancing the gameplay experience.

    Limit the narrative to 600 words in plaintext.
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


def is_solved(data) -> bool:
    try:
        if 'postid' not in data:
            raise ERROR.DB_Error("Missing postid")
        post = get_post(data)
        return post['posttype'] == 'solved'
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
