from flask import Flask, request, jsonify
from events_table import Event
from user_table import Followers, db

app = Flask(__name__)

@app.route('/search_events', methods=['GET'])
def search_events():
    date = request.args.get('date')
    time = request.args.get('time')
    events = Event.query.filter_by(date=date, time=time).all()
    return jsonify([event.to_dict() for event in events])

@app.route('/follow_event/<event_id>', methods=['POST'])
def follow_event(event_id):
    user_id = request.json['user_id']
    event = Event.query.get(event_id)
    if event:
        follower = Followers(event_id=event_id, user_id=user_id)
        db.session.add(follower)
        db.session.commit()
        event.followers += 1
        db.session.commit()
        return jsonify({'success': 'Event followed successfully'})
    return jsonify({'error': 'Event not found'}), 404

@app.route('/unfollow_event/<event_id>', methods=['POST'])
def unfollow_event(event_id):
    user_id = request.json['user_id']
    event = Event.query.get(event_id)
    if event:
        follower = Followers.query.filter_by(event_id=event_id, user_id=user_id).first()
        if follower:
            db.session.delete(follower)
            db.session.commit()
            event.followers -= 1
            db.session.commit()
            return jsonify({'success': 'Event unfollowed successfully'})
    return jsonify({'error': 'Event not found'}), 404

@app.route('/get_event_followers/<event_id>', methods=['GET'])
def get_event_followers(event_id):
    event = Event.query.get(event_id)
    if event:
        followers = Followers.query.filter_by(event_id=event_id).all()
        return jsonify([follower.to_dict() for follower in followers])
    return jsonify({'error': 'Event not found'}), 404