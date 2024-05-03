def get_data():
    """Get data from db for leaderboard"""
    return


def _process_data():
    """Process data for leaderboard"""
    return


def sort_data(data):
    """Sort data for leaderboard"""
    sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
    return sorted_data

