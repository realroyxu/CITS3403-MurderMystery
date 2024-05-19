# Murder Mystery Game / Forum
## Make sure you are either in WSL (Windows) or Linux/MacOS


## Purpose

The purpose of this web application is to provide a platform for users to solve murder mystery puzzles, participate in leaderboards, and interact through comments. The application is designed with a user-friendly interface and includes features such as user authentication, puzzle solving, commenting, and leaderboard tracking.

### Design and Use

- **User Authentication**: Users can register and log in to the application to access personalized features.
- **Sudoku Puzzle Solving**: Users can attempt various Sudoku puzzles. The application verifies solutions and tracks puzzle-solving times.
- **Comments**: Users can comment on puzzles and interact with other users.
- **Leaderboards**: The application maintains site-wide and post-specific leaderboards to track user performance based on post count and solve count.

## Group Members

| UWA ID     | Name              | GitHub Username  |
|------------|-------------------|------------------|
| 23455873   | Aifert Yet        | Aifert           |
| 23476285   | Ryan Allagapen    | Teylan           |
| 23993019   | Hongkang "Roy" Xu | RealRoyXu        |
| 23344707   | Jack Langoulant   | jacklangoulant  |

## Launching the Application
To launch the application, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/realroyxu/CITS3403-Sudoku.git
    cd into the repository
    ```

2. **Set Up the Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory of the project and add the following variables:
    ```plaintext
    SECRET_KEY=your_secret_key
    UPLOAD_FOLDER=app/static/uploads/
    SQLALCHEMY_DATABASE_URI=sqlite:///db/ormtest.db
    DEV_DATABASE_URL=sqlite:///dev.db
    TEST_DATABASE_URL=sqlite:///test.db
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Initialize the Database**:
    ```bash
    flask db upgrade
    ```

6. **Run the Application**:
    ```bash
    flask run --port 8000
    ```
    The application will be available at `http://127.0.0.1:8000`.


## Running the Tests

To run the tests for the application, follow these steps:

1. **Ensure the Virtual Environment is Activated**:
    ```bash
    source venv/bin/activate
    ```

2. **Set Up the Testing Environment Variables**:
    Make sure your `.env` file includes the `TEST_DATABASE_URL` variable.

3. **Run the Tests**:
    ```bash
    python -m unittest discover tests
    ```
    This command will discover and run all the tests located in the `tests` directory.

    Please note some tests may fail if your test.db include / does not include certain data, please adjust your db accordingly.
---
